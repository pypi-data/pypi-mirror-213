# Lab Partner

## to expose low ports 

```bash
echo "net.ipv4.ip_unprivileged_port_start=0" >> /etc/sysctl.conf
sysctl --system
```



