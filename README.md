# gammu

This role is designed to forward SMS to telegram or email. It disables `gammu-smsd` service and runs daemon under `runit`. May be used multiple times.

## requirements
[runit](https://github.com/hryamzik/ansible-role-runit.git) role
Ubuntu 16.04

## example

```yml
- hosts: pi
  become: yes
  roles:
    - name: gammu
      gammu_reporting:
        bot_key: "{{ telegram_key_user1 }}"
        chat_id: "{{ chat_id_user1 }}"
        mail_to: "{{ email_user1 }}"
      gammu_phoneid: user1
      gammu_device: /dev/ttyW810i
      tags: sms

    - name: gammu
      gammu_reporting:
        bot_key: "{{ telegram_key_user2 }}"
        chat_id: "{{ chat_id_user2 }}"
        mail_to: "{{ email_user2 }}"
      gammu_phoneid: orange
      gammu_device: /dev/ttyHuaweiOrange00
      tags: sms
``` 

You may also find udev rules example useful:

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
