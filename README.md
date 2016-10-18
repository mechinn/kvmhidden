kvmhidden vdsm hook
=================================
VDSM Hook for hiding kvm from the vm

Installation:
* Use engine-config to set the appropriate custom properties as such:

Custom property for a VM:
    sudo engine-config -s "UserDefinedVMProperties=kvmhidden=^(true|false)$"

* Verify that the custom properties were added properly:
    sudo engine-config -g UserDefinedVMProperties

Usage:
In the VM configuration window, open the custom properties tab
and add kvmhidden=true to hide kvm from the vm.

Details:
Adds the following to the vdsm xml

```xml
  <features>
    ...
    <kvm>
      <hidden state='on'/>
    </kvm>
  </features>
```