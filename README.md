# gammu

This role is designed to install multiple `gammu-smsd` services with `runit`. It disables `gammu-smsd` service and runs daemon under `runit`. May be used multiple times.

## requirements
[runit](https://github.com/hryamzik/ansible-role-runit.git) role
Ubuntu 16.04
Valid template ```gammu_template_name``` variable, default configuration doens't make much sense.

## example

```yml
- hosts: pi
  become: yes
  roles:
    - name: gammu
      gammu_template_name: etc/gammu.d/gammu-smsdrc-user1.j2
      gammu_device: /dev/ttyW810i
      gammu_phoneid: phone1
      tags: sms

    - name: gammu
      gammu_template_name: etc/gammu.d/gammu-smsdrc-user2.j2
      gammu_phoneid: orange
      gammu_device: /dev/ttyHuaweiOrange00
      tags: sms
``` 

You may also find `udev` rules example useful:

`99-usb-serial.rules`

```
SUBSYSTEM=="tty", ATTRS{idVendor}=="12d1", ATTRS{idProduct}=="1001", SYMLINK+="ttyHuaweiOrange%E{ID_USB_INTERFACE_NUM}"
SUBSYSTEM=="tty", ATTRS{idVendor}=="0fce", ATTRS{idProduct}=="d042", SYMLINK+="ttyW810i"
```

And `udev` handlerL

```yml
- name: reload udev
  shell: udevadm control --reload-rules && udevadm trigger
````
