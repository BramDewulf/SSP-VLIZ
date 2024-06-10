# Use the official GROBID image as the base image (latest image)
FROM grobid/grobid:latest

# Expose the port GROBID will be running on
EXPOSE 8070 

# Start GROBID service
CMD ["./gradlew", "run"]