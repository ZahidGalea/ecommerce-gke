import argparse
import sys

import anyio
import dagger


async def main(project_id, app_version):
	config = dagger.Config(log_output=sys.stdout)

	async with dagger.Connection(config) as client:
		# use a node:16-slim container
		# mount the source code directory on the host
		# at /src in the container
		source = (
			client.container()
			.from_("instrumentisto/flutter:latest")
			.with_directory(
					"/app",
					client.host().directory("ecommerce_front_app/"),
					exclude=[".idea/", ".dart_tool/"],
			).with_workdir("/app")
		)

		# run application tests
		test = source.with_exec(["flutter", "test"])

		# build application
		# write the build output to the host
		await (
			test.with_exec(["flutter", "build", "web"])
			.directory("./build")
			.export("./build")
		)

		# highlight-start
		# use an nginx:alpine container
		# copy the build/ directory into the container filesystem
		# at the nginx server root
		# publish the resulting container to a registry
		image_ref = await (
			client.container()
			.from_("nginx:1.23-alpine")
			.with_directory("/usr/share/nginx/html", client.host().directory("./build"))
			.publish(f"gcr.io/{project_id}/flutter-app:{app_version}")
		)

	print(f"Published image to: {image_ref}")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process environment variables.')
	parser.add_argument('-e', '--env', default='prod', help='Environment variable')
	parser.add_argument('--front_version', required=True, help='Front version')
	parser.add_argument('--gcp_project_id', required=True, help='Google Cloud Platform Project ID')
	args = parser.parse_args()

	anyio.run(main, args.gcp_project_id, args.front_version)
