podman machine ssh -- -G

# will see

port 58958
identityfile C:\Users\你的用戶名\.local\share\containers\podman\machine\machine


ssh -i "C:\Users\gostj\.local\share\containers\podman\machine\machine" -p 58958 -N -o GatewayPorts=yes -L 0.0.0.0:4173:localhost:4173 root@localhost