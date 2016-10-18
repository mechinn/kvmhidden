#!/usr/bin/python
import os
import sys
import argparse
import traceback

features_tag = 'features'
kvm_tag = 'kvm'
hidden_tag = 'hidden'

def kvmhidden(domxml):
    features = domxml.getElementsByTagName(features_tag)
    if len(features) > 0:
        kvms = features[0].getElementsByTagName(kvm_tag)
        if len(kvms) > 0:
            hiddens = kvms[0].getElementsByTagName(hidden_tag)
            if len(hiddens) > 0:
                sys.stderr.write('kvmhidden: setting hidden to on')
                set_state_on(hiddens[0])
            else:
                sys.stderr.write('kvmhidden: hidden does not exist creating')
                create_append(kvms[0],domxml,[hidden_tag],[set_state_on])
        else:
            sys.stderr.write('kvmhidden: kvm does not exist creating')
            create_append(features[0],domxml,[hidden_tag,kvm_tag],[set_state_on,create_append])
    else:
        sys.stderr.write('kvmhidden: features do not exist creating')
        create_append(domxml.firstChild,domxml,[hidden_tag,kvm_tag,features_tag],[set_state_on,create_append,create_append])
    return domxml

def create_append(element,domxml,tags,funcs):
    new_element = domxml.createElement(tags.pop())
    funcs.pop()(new_element,domxml,tags,funcs)
    return element.appendChild(new_element)

def set_state_on(element,domxml=None,tags=None,funcs=None):
    element.setAttribute('state', 'on')

def testfile():
    from xml.dom.minidom import parse
    domxml = parse('test.xml')
    domxml = kvmhidden(domxml)
    print(domxml.toprettyxml())

def hook():
    import hooking
    if hooking.tobool(os.environ.get('kvmhidden')):
        try:
            domxml = hooking.read_domxml()
            domxml = kvmhidden(domxml)
            hooking.write_domxml(domxml)
        except:
            sys.stderr.write('kvmhidden: [unexpected error]: %s\n' % traceback.format_exc())
            sys.exit(2)

def main():
    parser = argparse.ArgumentParser(description='VDSM Hook for hiding kvm from the vm')
    parser.add_argument('--debug', action='store_true',
        help='Run this in debug mode for testing xml file and printing output')
    args = parser.parse_args()
    if args.debug:
        testfile()
    else:
        hook()

if __name__ == '__main__':
    main()