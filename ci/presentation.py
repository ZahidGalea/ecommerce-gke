import argparse
import sys

import dagger
from dagger import Container

PRESENTATION_APP_FOLDER = "services/presentation"


def main(project_id, app_version):
	config = dagger.Config(log_output=sys.stdout)

	with dagger.Connection(config) as client:
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
		test = source.with_exec(["flutter", "test"])

		# build application
		# write the build output to the host
		build = (
			test.with_exec(["flutter", "build", "web"])
			.directory("./build")
			.export(f"./{PRESENTATION_APP_FOLDER}/build")
		)

		print(build)

		# Flutter app push up
		flutter_app_container: Container = client.container().build(
				context=client.host().directory(f"./{PRESENTATION_APP_FOLDER}"))

		flutter_app_container.publish(f"us-east1-docker.pkg.dev/{project_id}/presentation/flutter-app:{app_version}")
		flutter_app_container.publish(f"us-east1-docker.pkg.dev/{project_id}/presentation/flutter-app:latest")

	print(f"Published image to: {flutter_app_container}")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process environment variables.')
	parser.add_argument('--gcp_project_id', required=True, help='Google Cloud Platform Project ID')


	def get_version():
		with open(f"{PRESENTATION_APP_FOLDER}/VERSION", "r") as version_file:
			return version_file.read().strip()


	version = get_version()

	args = parser.parse_args()
	main(args.gcp_project_id, version)
