import argparse
import sys

import anyio
import dagger
from dagger import Container

PRESENTATION_APP_FOLDER = "services/presentation"


async def main(project_id, app_version, environment):
	config = dagger.Config(log_output=sys.stdout)

	async with dagger.Connection(config) as client:
		# Testing with flutter docker container
		source = (
			client.container()
			.from_("instrumentisto/flutter:latest")
			.with_directory(
					"/app",
					client.host().directory(f"{PRESENTATION_APP_FOLDER}/"),
					exclude=[".idea/", ".dart_tool/"],
			).with_workdir("/app")
		)

		# Run application tests
		test = await source.with_exec(["flutter", "test"])

		# build application
		# write the build output to the host
		build = await (
			test.with_exec(["flutter", "build", "web"])
			.directory("./build")
			.export(f"./{PRESENTATION_APP_FOLDER}/build")
		)

		print(build)

		# Flutter app push up
		flutter_app_container: Container = client.container().build(
				context=client.host().directory(f"./{PRESENTATION_APP_FOLDER}"))

		await flutter_app_container.publish(
				f"us-east1-docker.pkg.dev/{project_id}/presentation-{environment}/flutter-app:{app_version}")
		await flutter_app_container.publish(
				f"us-east1-docker.pkg.dev/{project_id}/presentation-{environment}/flutter-app:latest")

		helm_deploy_string = ["helm", "upgrade", f"ecommerce-{environment}", ".", "--namespace",
							  f"ecommerce-{environment}",
							  "--install",
							  '--create-namespace',
							  "--dependency-update",
							  '--wait', "--debug",
							  "--set",
							  f"presentation_image=us-east1-docker.pkg.dev/{project_id}/presentation-{environment}/flutter-app:{app_version}"]

	# Helm deployment
	# helm = client.container() \
	# 	.from_("alpine/helm") \
	# 	.with_directory("/app", client.host().directory(f"{PRESENTATION_APP_FOLDER}/helm")) \
	# 	.with_workdir("/app")
	print(f"Deploy: {' '.join(helm_deploy_string)}")
	print(f"Upgrading helm ecommerce-{environment} setting front_version={app_version}")
	print(f"Published to: us-east1-docker.pkg.dev/{project_id}/presentation-{environment}/flutter-app:{app_version}")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process environment variables.')
	parser.add_argument('--gcp_project_id', required=True, help='Google Cloud Platform Project ID')
	parser.add_argument('--env', required=False, default="dev", help='Environment')


	def get_version():
		with open(f"{PRESENTATION_APP_FOLDER}/VERSION", "r") as version_file:
			return version_file.read().strip()


	version = get_version()

	args = parser.parse_args()
	anyio.run(main, args.gcp_project_id, version, args.env)
