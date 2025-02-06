docker build -t ghcr.io/aliaflore/licenta:nginx . --target nginx --push
docker build -t ghcr.io/aliaflore/licenta:backend . --target production --push
docker build -t ghcr.io/aliaflore/licenta:frontend . --target frontend --push