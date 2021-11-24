include etc/environment.sh

unittest:
	python3 -m unittest discover --buffer
coverage:
	coverage run --omit=test/* -m unittest discover --buffer
	coverage report -m
	coverage html --directory reports

lambda: lambda.package.signed lambda.deploy
lambda.package.signed:
	sam package -t ${LAMBDA_TEMPLATE} --output-template-file ${LAMBDA_OUTPUT} --s3-bucket ${S3BUCKET} --signing-profiles ${SIGNING_PROFILES}
lambda.deploy:
	sam deploy -t ${LAMBDA_OUTPUT} --stack-name ${LAMBDA_STACK} --parameter-overrides ${LAMBDA_PARAMS} --capabilities CAPABILITY_NAMED_IAM
lambda.deploy.signed:
	sam deploy -t ${LAMBDA_OUTPUT} --stack-name ${LAMBDA_STACK} --parameter-overrides ${LAMBDA_PARAMS} --signing-profiles ${SIGNING_PROFILES} --capabilities CAPABILITY_NAMED_IAM
lambda.continue.rollback:
	aws cloudformation continue-update-rollback --stack-name ${LAMBDA_STACK}

lambda.local:
	sam local invoke -t ${LAMBDA_TEMPLATE} --parameter-overrides ${LAMBDA_PARAMS} --env-vars etc/envvars.json -e etc/event.json Fn | jq
lambda.invoke.sync:
	aws --profile ${PROFILE} lambda invoke --function-name ${O_FN} --invocation-type RequestResponse --payload file://etc/event.json --cli-binary-format raw-in-base64-out --log-type Tail tmp/fn.json | jq "." > tmp/response.json
	cat tmp/response.json | jq -r ".LogResult" | base64 --decode
	cat tmp/fn.json | jq
lambda.invoke.async:
	aws --profile ${PROFILE} lambda invoke --function-name ${O_FN} --invocation-type Event --payload file://etc/event.json --cli-binary-format raw-in-base64-out --log-type Tail tmp/fn.json | jq "."

signer: signer.package signer.deploy
signer.package:
	sam package -t ${SIGNER_TEMPLATE} --output-template-file ${SIGNER_OUTPUT} --s3-bucket ${S3BUCKET}
signer.deploy:
	sam deploy -t ${SIGNER_OUTPUT} --stack-name ${SIGNER_STACK} --parameter-overrides ${SIGNER_PARAMS} --capabilities CAPABILITY_NAMED_IAM

signer.list.platforms:
	aws signer list-signing-platforms | jq '.platforms[] | {"platformId": .platformId, "partner": .partner, "target": .target}'
signer.list.profiles:
	aws signer list-signing-profiles | jq