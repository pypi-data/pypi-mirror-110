import argparse
import logging
from pkg_resources import get_distribution
import sys

from . import blobs, deobfuscate, email, hashes, hostname, ip, url


logger = logging.getLogger(name=__name__)


REFANGING_MODULES = [url, email, hostname, ip]


def extract_all(text, refang=False, blob_text_depth=1, **blob_decode_kwargs):
	for module in REFANGING_MODULES:
		yield from module.extract(text=text, refang=refang)

	yield from hashes.extract(text=text)
	for blob_text in blobs.extract_text(
			text=text, depth=blob_text_depth, **blob_decode_kwargs):
		yield blob_text
		yield from extract_all(
			text=blob_text, refang=refang, blob_text_depth=0)


def main():
	package_name, *_ = __name__.split('.', 1)
	package_version = get_distribution(package_name).version
	root_parser = argparse.ArgumentParser(
		description='Indicator of Compromise (IOC) Detection')

	root_parser.add_argument(
		'-V', '--version',
		action='version',
		version=f'%(prog)s {package_version}',
	)
	root_parser.add_argument(
		'-l', '--log-level', default='INFO', help='Set the log level')
	root_parser.add_argument(
		'-r', '--refang', action='store_true', help='Refang detected IOCs')
	root_parser.add_argument(
		'--raw',
		action='store_true',
		help="Don't normalise input text before scanning for IOCs",
	)

	root_parser.set_defaults(function=extract_all)

	subparsers = root_parser.add_subparsers()
	
	all_parser = subparsers.add_parser(
		'all', description='Extract all IOC types')
	all_parser.set_defaults(function=extract_all)

	blobs_parser = subparsers.add_parser(
		'blobs', description='Extract embedded binary blobs')
	blobs_parser.set_defaults(function=blobs.extract)

	email_parser = subparsers.add_parser(
		'email', description='Extract email addresses')
	email_parser.set_defaults(function=email.extract)

	hashes_parser = subparsers.add_parser(
		'hashes', description='Extract hash values')
	hashes_parser.set_defaults(function=hashes.extract)

	hostname_parser = subparsers.add_parser(
		'hostname', description='Extract hostnames')
	hostname_parser.set_defaults(function=hostname.extract)

	ip_parser = subparsers.add_parser('ip', description='Extract IP addresses')
	ip_parser.set_defaults(function=ip.extract)

	url_parser = subparsers.add_parser('url', description='Extract URLs')
	url_parser.set_defaults(function=url.extract)

	secrets_parser = subparsers.add_parser(
		'secrets', description='Extract text from embedded binary blobs')
	secrets_parser.set_defaults(function=blobs.extract_text)

	normalise_parser = subparsers.add_parser(
		'normalise', description='Output the normalised input text')
	normalise_parser.set_defaults(function=deobfuscate.normalise)

	namespace = root_parser.parse_args(sys.argv[1:])
	arguments = vars(namespace)

	log_level = arguments.pop('log_level')
	logging.basicConfig(level=log_level.upper())
	logger.debug('parsed args: %r', namespace)

	in_file = sys.stdin
	out_file = sys.stdout

	text = in_file.read()
	if not namespace.raw:
		text = deobfuscate.normalise(text)

	command_function = namespace.function
	if command_function is hashes.extract:
		out_values = hashes.extract(text=text)
	elif command_function is blobs.extract_text:
		out_values = blobs.extract_text(text=text)
	elif command_function is deobfuscate.normalise:
		out_file.write(command_function(text=text))
		return
	else:
		out_values = command_function(text=text, refang=namespace.refang)

	out_file.writelines(f'{v}\n' for v in out_values)
