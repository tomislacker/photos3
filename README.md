# PhotoS3
Hopefully to be photo album based in S3 with event driven processing.

This has started as a pet project to keep me busy and learning/playing while
I'm not working.

## Roadmap
- Infrastructure entirely managed by [CloudFormation]
- [S3] storage of images
- Event-driven [Exif] metadata extraction & storage
- Subject matter classification by [Rekognition]
- [API Gateway]
  - Authentication/authorization
  - Image search

## References
- https://hub.docker.com/_/amazonlinux/
- https://cloudonaut.io/integrate-sqs-and-lambda-serverless-architecture-for-asynchronous-workloads/
- https://github.com/zwily/sqs-to-lambda-via-lambda
- https://pypi.python.org/pypi/ExifRead
- http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-deployment-pkg.html
- http://mt.wiglaf.org/aaronm/2016/11/s3-triggered-lambda-via-beanstalk.html
- http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html

[API Gateway]: https://aws.amazon.com/api-gateway/ "AWS API Gateway"
[Exif]: https://en.wikipedia.org/wiki/Exif
[Rekognition]: https://aws.amazon.com/rekognition/ "AWS Rekognition"
[S3]: https://aws.amazon.com/s3/ "AWS S3"
[CloudFormation]: https://aws.amazon.com/cloudformation/ "AWS CloudFormation"
