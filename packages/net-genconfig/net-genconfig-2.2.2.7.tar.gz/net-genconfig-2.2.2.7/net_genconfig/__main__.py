# net_genconfig.__main__



import net_genconfig

import argparse
from copy import deepcopy
from functools import reduce
import jinja2
import os
import re
import sys
import yaml

from deepops import deepget, deepmerge, deepremoveitems

from net_genconfig import helpers, netaddr_filter

from net_inventorylib import NetInventory



# --- definitions ---



# dictionary of imported global helper functions to be added to the
# Jinja2 environment
#
# the key is the name of the function available in Jinja2 and the value
# is the reference to that function (here, imported from the deepops
# module)

deep_helpers = {
    "deepcopy": deepcopy,
    "deepmerge": deepmerge,
    "deepremoveitems": deepremoveitems
}



# --- functions ---



def render_file(name, env, output_filename=None, no_output=False,
                no_squash_blanklines=False, comment_prefix=None, debug=False,
                **render_vars):

    """Read a configuration template file and render it.

    The name of the file will be found in the supplied Jinja2
    environment so cannot just be an absolute patht to a file.  '.j2'
    will be appended to the name.

    The render_vars will be passed to the Jinja2 render() method to
    provide variables.  These will typically by the devicename, device
    object and inventory but can be omitted when running a test
    template (as it isn't a proper template but just one to test things
    out in).

    The return value is True if the template could be rendered and
    False if not.
    """


    filename = name + ".j2"


    # try to load the template using the supplied environment (which includes
    # the directory search paths, so will be relative to those)

    try:
        template = env.get_template(filename)

    except jinja2.exceptions.TemplateNotFound:
        print("warning: template file not found in environment: %s - skipping"
                  % filename,
              file=sys.stderr)

        return False


    # render the template configuration

    config = template.render(**render_vars)


    # return (successfully), if output is disabled

    if no_output:
        if debug:
            print("debug: output disabled", file=sys.stderr)

        return True


    # if we have a prefix for comment stripping set, remove lines
    # beginning with that (then we can remove consecutive blank lines
    # next)

    if comment_prefix:
        non_comment_config_lines = [
            l for l in config.split("\n")
                if not re.match(r"^\s*%s(\s+[^\n]*|)$" % comment_prefix, l)]

        config = "\n".join(non_comment_config_lines)


    # if not disabled, squash blank lines

    if not no_squash_blanklines:
        # remove any blank lines at the top
        config = re.sub(r"^\n+", "", config)

        # squash three or more blank lines into two (a single blank
        # line)
        config = re.sub(r"\n\n\n+", r"\n\n", config)

        # the last line should end with a single newline
        config = re.sub(r"\n\n+$", r"\n", config)

    # write output to either standard output or a file, depending on
    # the options specified

    if output_filename:
        output_filename_expanded = output_filename.replace("%", devicename)

        if debug:
            print("debug: writing to output file: %s"
                      % output_filename_expanded,
                  file=sys.stderr)

        with open(output_filename_expanded, "w") as output_file:
            print(config, file=output_file)

    else:
        if debug:
            print("debug: writing to standard output", file=sys.stderr)

        print(config)


    # rendering succeeded

    return True



def deepselect(d, *p):
    """Return the specified portion of the nested structure d given by
    the path p, as per deepops.deepget() but also prefix the path as a
    leading path.

    This has the effect of returning structure d with only the portion
    given by p and nothing else and is useful for highlighting the path
    into the structure.

    If the path could not be found, None is returned, without the path
    prefix, highlighting that it was not found (as opposed to being
    empty).  This is useful in the context this is used.
    """

    # copy and reverse the path so we can use reduce() to fold right
    r = list(p)
    r.reverse()

    # try to get the path into the structure, returning None if it was
    # not found (not prefixing the path), to illustrate that the key
    # could not be found
    try:
        d_sub = deepget(d, *p, default_error=True)
    except KeyError:
        return None

    # build the path in with the final value as the deepget()
    return reduce(lambda d, k: { k: d }, r, d_sub)



def render_config(devicename, inventory, env, output_filename,
                  no_output=False, no_squash_blanklines=False,
                  comment_prefix=None, dump_device=False, debug=False, **vars):

    """Render the configuration for the specified device and write it
    to either standard output or a file, depending on the command line
    options specified.

    The configuration will be generated from a template file which is
    found in the Jinja2 environment, with the filename based on the
    platform and role.  This rendering is done by render_file().

    Returns True if the configuration is generated successfully.  If
    there is a problem of some sort which is not serious enough to
    abort the script (such as one device cannot be found), the function
    will return False.  More serious problems will stop the entire
    script.
    """


    if devicename not in inventory["devices"]:
        print("warning: device not found in inventory: %s - skipping"
                  % devicename,

              file=sys.stderr)

        return False


    # get the definition dictionary for this device from the inventory
    #
    # we use this variable for some checks here, and to pass it to the
    # starting role template, so it avoids repeatedly fetching it

    device = inventory["devices"][devicename]

    if device is None:
        print("warning: device definition empty: %s - skipping" % devicename,
              file=sys.stderr)

        return False


    # if the dump device option is enabled, print a YAML version of the
    # device definition (now we've done merges, etc.) to stdout and
    # return

    if dump_device:
        print(yaml.dump(device, default_flow_style=False))
        return True


    # we need a role and platform to read in the template file

    if "role" not in device:
        print("error: missing role for device: %s" % devicename,
              file=sys.stderr)

        exit(1)

    if "platform" not in device:
        print("error: missing platform for device: %s" % devicename,
              file=sys.stderr)

        exit(1)

    role = device["role"]
    platform = device["platform"]


    if debug:
        print("debug: generating configuration for: %s role: %s "
                  "platform: %s" % (devicename, role, platform),
              file=sys.stderr)


    # work out the filename of the template for the platform and role

    role_filename = os.path.join(platform, role)

    if debug:
        print("debug: using role file (relative to filesystem loader "
                  "directory): %s" % role_filename,
               file=sys.stderr)


    # render the template configuration file

    if not render_file(role_filename, env, output_filename, no_output,
                       no_squash_blanklines, comment_prefix,
                       devicename=devicename, device=device,
                       inventory=inventory, **vars):

        print("warning: failed to render template for: %s - skipping"
                  % devicename,
              file=sys.stderr)

        return False


    # rendering succeeded

    return True



# --- command line arguments ---



# create the parser and add in the available command line options

parser = argparse.ArgumentParser(
    # override the program name as running this as a __main__ inside a
    # module directory will use '__main__' by default - this name isn't
    # necessarily correct, but it looks better than that
    prog="net-genconfig",

    # we want the epilog help output to be printed as it and not
    # reformatted or line wrapped
    formatter_class=argparse.RawDescriptionHelpFormatter)


parser.add_argument(
    "-C", "--config",
    dest="config_dirname",
    default=(os.environ.get("NET_CONFIG_DIR")
                 if "NET_CONFIG_DIR" in os.environ else "."),
    help="base directory for roles, include and inventory")

parser.add_argument(
    "-r", "--roles",
    dest="roles_dirname",
    default="roles",
    help="directory containing role configuration templates")

parser.add_argument(
    "-n", "--include",
    dest="include_dirname",
    default="include",
    help="directory containing included templates / macro libraries")

parser.add_argument(
    "-i", "--inventory",
    dest="inventory_dirname",
    default="inventory",
    help="directory containing inventory of devices, networks, etc.")

parser.add_argument(
    "-o", "--output",
    dest="output_filename",
    help="write configuration to named file instead of stdout; '%%' "
         "can be used to substitute in the name of the device into the "
         "filename")

parser.add_argument(
    "-O", "--no-output",
    action="store_true",
    help="generate the configuration but do not output it - useful to "
         "test generation succeeds")

parser.add_argument(
    "-s", "--no-squash-blanklines",
    action="store_true",
    help="disable the squashing of leading and trailing, as well as "
         "multiple, consecutive blank lines (prevent equivalent of '| "
         "cat -s') in output")

parser.add_argument(
    "-M", "--comment-prefix",
    default="##",
    help="prefix for comments to strip from output (useful if the "
         "target platform does not natively support comments but they "
         "are to be used to provide a documented configuration; set to "
         "'-' to disable stripping")

parser.add_argument(
    "-E", "--list-env",
    action="store_true",
    help="list filter and global helper functions and stop (this will "
         "include the standard Jinja2, as well as the netaddr module "
         "and custom ones)")

parser.add_argument(
    "-I", "--dump-inventory",
    action="store_true",
    help="dump complete read inventory in YAML to stdout and stop, "
         "without generating any configurations")

parser.add_argument(
    "-F", "--dump-filepaths",
    action="store_true",
    help="dump paths of files which are the source of each entry in "
         "the inventory")

parser.add_argument(
    "-U", "--dump-device",
    action="store_true",
    help="dump resulting device definition in YAML to stdout, after "
         "merging profiles and stop, without generating any "
         "configurations")

parser.add_argument(
    "-S", "--subtree-dump-filter",
    metavar="key",
    nargs="*",
    default=[],
    help="limit dump options for the inventory and file paths to "
         "subtree of configuration dictionary with a path specified as "
         "list of keys; '-' can be used to represent None and values "
         "that are parsable as integers will be converted to integers")

parser.add_argument(
    "-d", "--define",
    action="append",
    nargs=2,
    default=[],
    help="define variable for use in the template",
    metavar=("VAR", "VALUE"))

parser.add_argument(
    "-T", "--template",
    dest="template_filename",
    help="read the inventory, set up the environment and then render "
         "the specified template file (from the roles or include "
         "directories) then stop - used to quickly test template "
         "functions without needing to construct a device")

parser.add_argument(
    "-q", "--quiet",
    action="store_true",
    help="when generating configuration for multiple devices, don't "
         "print the name of each device, as it's generated")

parser.add_argument(
    "-D", "--debug",
    action="store_true",
    help="enable debug mode")

parser.add_argument(
    "-R", "--raise-exception",
    action="store_true",
    help="when an exception is explicitly raised through a helper "
         "function, raise the complete exception rather than catch it "
         "and just print the message specific error message - this is "
         "useful if the exception does not make it clear where it "
         "occurred")

parser.add_argument(
    "devicename",
    nargs="*",
    help="name(s) of the device(s) to generate the configuration for")

parser.add_argument(
    "--version",
    action="version",
    version=("%(prog)s " + net_genconfig.__version__))


# parse the supplied command line against these options, storing the
# results

args = parser.parse_args()

roles_dirname = os.path.join(args.config_dirname, args.roles_dirname)
include_dirname = os.path.join(args.config_dirname, args.include_dirname)
inventory_dirname = os.path.join(args.config_dirname, args.inventory_dirname)
output_filename = args.output_filename
no_output = args.no_output
no_squash_blanklines = args.no_squash_blanklines
comment_prefix = None if args.comment_prefix == "-" else args.comment_prefix
list_env = args.list_env
dump_inventory = args.dump_inventory
dump_filepaths = args.dump_filepaths
dump_device = args.dump_device
subtree_dump_filter = args.subtree_dump_filter
template_filename = args.template_filename
quiet = args.quiet
devicenames = args.devicename
debug = args.debug
raise_exception = args.raise_exception

vars = {}
for var, value in args.define:
    vars[var] = value


if debug:
    print("""\
debug: roles directory: %s
debug: include directory: %s
debug: inventory directory: %s
debug: output filename: %s
debug: device names: %s"""
              % (roles_dirname, include_dirname, inventory_dirname,
                 output_filename, devicenames),
          file=sys.stderr)


# if a subtree was specified for debugging 'dump' options, handle some
# special cases of the elements in the path:
#
# * a single dash ('-') is treated as None
#
# * if the element can be converted to an integer, do that, rather than
#   treat it as a string
#
# these are to cope with limitations on the parsing available in the
# ArgumentParser class compared with the flexibility and ambiguity of
# the configuration dictionary

if subtree_dump_filter:
    def convert_path_item(s):
        "Convert a single path element from a string into another type."

        if s == "-":
            return None

        try:
            return int(s)
        except ValueError:
            pass

        return s

    subtree_dump_filter = [ convert_path_item(s) for s in subtree_dump_filter]


# check that the roles and include directories exist

if not os.path.isdir(roles_dirname):
    print("error: roles directory does not exist: %s" % roles_dirname,
            file=sys.stderr)

    exit(1)

if not os.path.isdir(include_dirname):
    print("error: include directory does not exist: %s" % include_dirname,
            file=sys.stderr)

    exit(1)


# check a couple of nonsensical configurations aren't being use related
# to multiple devices

if (len(devicenames) > 1) and (not (no_output or dump_device)):
    if not output_filename:
        print("error: multiple device names specified but outputting "
                  "to standard output - all configurations would be "
                  "concatenated",
              file=sys.stderr)

        exit(1)

    elif output_filename.find("%") == -1:
        print("error: multiple device names specified but output "
                  "filename does not contain a '%' to substitute the "
                  "device name - output file would be overwritten",
              file=sys.stderr)

        exit(1)



# --- inventory ---



if debug:
    print("debug: starting to read inventory directory", file=sys.stderr)



# read in the inventory

inventory = NetInventory(inventory_dirname, debug=debug)


if dump_inventory:
    print(yaml.dump(deepselect(dict(inventory), *subtree_dump_filter),
          default_flow_style=False))
    exit(0)

if dump_filepaths:
    print(yaml.dump(deepselect(inventory.get_filepaths(),
                               *subtree_dump_filter),
                    default_flow_style=False))
    exit(0)

if "devices" not in inventory:
    print("error: no devices found in inventory", file=sys.stderr)
    exit(1)



# --- jinja2 ---



# build the Jinja2 environment

jinja_fsloader_dirs = [roles_dirname, include_dirname]

if debug:
    print("debug: creating environment with filesystem loader directories: "
          "%s" % jinja_fsloader_dirs)

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(jinja_fsloader_dirs),
    extensions=[
        "jinja2.ext.do", "jinja2.ext.loopcontrols"],
    trim_blocks=True)


# add in the special warn(), raise() and assert() functions, as well as
# some other functions we need, into the Jinja2 environment

for helpers_dict in [deep_helpers, helpers.helpers]:
    for helper in helpers_dict:
        env.globals[helper] = helpers_dict[helper]


# add in the netaddr library functions as additional filters

for filter_name, filter_func in (
    netaddr_filter.FilterModule().filters().items()):

    env.filters[filter_name] = filter_func


# if the 'list environment' option is specified, print out the filter
# and global helper functions and stop

if list_env:
    print("Filters:")
    for filter in sorted(env.filters):
        print("  " + filter)

    print()

    print("Global helpers:")
    for global_helper in sorted(env.globals):
        print("  " + global_helper)

    exit(0)



# --- render ---



# if a template file has been specified directly (for testing) then
# render that directly and stop

if template_filename:
    render_file(template_filename, env, output_filename, no_output,
                no_squash_blanklines, debug, inventory=inventory)

    exit(0)


# go through all the devices specified, generate and write out their
# configurations

if not devicenames:
    print("warning: no device names specified", file=sys.stderr)


# this flag will change to False if any configuration fails to render
# and is used to affect the return code from the script

complete_success = True


for devicename in devicenames:
    if (not quiet) and (len(devicenames) > 1):
        print(devicename)

    try:
        complete_success &= render_config(devicename, inventory, env,
                                          output_filename, no_output,
                                          no_squash_blanklines, comment_prefix,
                                          dump_device, debug, **vars)

    except helpers.HelperBaseException as e:
        # one of the explicit helper exceptions has occurred


        # if we're raising an exception anyway, do that; if not, just
        # print the exception text in the form of a user-friendly error
        # message

        if raise_exception:
            raise

        print("error:", e, file=sys.stderr)


        # since something went wrong, we don't have 'complete success'

        complete_success = False


exit(0 if complete_success else 1)
