import argparse
import os
import sys

import anyio
import dagger
from dagger.api.gen_sync import Container, Directory, Host, Secret


# Some tips. If you are using WSL2, the docker containers may not be on default linux location, u will have to change
# the runner mount with this path: /mnt/wsl/docker-desktop-data/version-pack-data/community/docker/containers

async def main(environment: str, gcp_credential_content: str, apply: bool = False, terraform_version='1.5.2'):
	if environment not in ['dev', 'prod']:
		raise Exception('Environment must be valid')

	config = dagger.Config(log_output=sys.stdout)

	# initialize Dagger client
	async with dagger.Connection(config) as client:
		client.pipeline = 'terraform'
		host: Host = client.host()
		infrastructure: Directory = host.directory("infrastructure")
		secrets: Directory = host.directory("secrets")

		# Secret mount
		# gcp_secret: File = secrets.file(gcp_credential_path)
		# gcp_secret_content = await gcp_secret.contents()
		gcp_secret: Secret = client.set_secret('gcp_credential', gcp_credential_content)
		# Init
		container: Container = client.container()
		container = container.from_(f"hashicorp/terraform:{terraform_version}")
		container = container.with_workdir('/application')
		container = container.with_user('root')
		# Mount folders
		container = container.with_directory('infrastructure', infrastructure)
		# Move to required environment
		container = container.with_workdir(f'infrastructure/{environment}')
		workdir = await container.workdir()
		print(f"Using terraform in {workdir}")
		# container entrypoint is terraform bin.

		container = container.with_mounted_secret('gcp_secret', gcp_secret)
		container = container.with_env_variable('GOOGLE_APPLICATION_CREDENTIALS', 'gcp_secret')

		# execution
		version = await container.with_exec('version').stdout()
		print(f"Hello from Dagger and {version}")

		# Init
		print('Terraform Init')
		container = container.with_exec(f'init')

		# Plan
		print('Terraform planning')
		container = container.with_exec((f'plan', '-out', 'tfplan'))

		if apply:
			print('Terraform Apply')
			container = container.with_exec((f'apply', 'tfplan'))

		await container.exit_code()
		print('Everything succeeded')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process environment variables.')
	parser.add_argument('-e', '--env', default='prod', help='Environment variable')
	parser.add_argument('-g', '--gcp_creds', required=True, help='Google Cloud Platform credentials')
	parser.add_argument('-a', '--apply', action=argparse.BooleanOptionalAction, help='Apply')
	args = parser.parse_args()
	# For pycharm usage in combination env var with params.
	if args.gcp_creds == "$GCP_CRED":
		args.gcp_creds = os.environ.get("GCP_CRED")

	anyio.run(main, args.env, args.gcp_creds, args.apply)
