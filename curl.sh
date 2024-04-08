https://api.intra.42.fr/oauth/authorize?FORTYTWO_API_KEY=u-s4t2ud-12c57e708b315daf0c44bb3ccdacaa14f1d142926cb04721324333e0a4a349c8&response_type=code&redirect_uri=http://127.0.0.1:8000

curl -F grant_type=authorization_code \
-F FORTYTWO_API_KEY=u-s4t2ud-12c57e708b315daf0c44bb3ccdacaa14f1d142926cb04721324333e0a4a349c8 \
-F FORTYTWO_API_SECRET=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 \
-F code=f0eb4445f32ab611cfa453581063525b999fa1629e7b7288aefb56c31ba41df1 \
-F redirect_uri=http://127.0.0.1:8000 \
-X POST https://api.intra.42.fr/oauth/token