# SteemStats (This is the sample with only one feature)
A Multifunctional Steem Discord Bot delevloped by @dhaka.witness


# Discord Bot Docker Deployment
This README outlines the steps necessary to build, run, and deploy a Discord bot within a Docker container. Ensure you have Docker installed and running on your machine before following these steps.

## Prerequisites
1. Docker
2. Discord Bot Token (from the Discord Developer Portal)

## Setup
Clone this repository to your local machine:
```
git clone <repository-url>
cd <repository-directory>
```
## Config the Bot file
To edit the bot file use ```nano```, go to the folder folder directory ```nano SteemStats.py``` then replace ```my bot token``` with your discord bot token and save.

## Building the Docker Image
Build the Docker image using:
```
docker build -t <your_container> .
```
## Running the Bot
To run your Discord bot within the Docker container, use:
```
docker run -d --name <your_container> <your-bot-name>
```
## Check the logs
```
docker logs <your_container>
```
## Contributing
Contributions are what makes the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

## Contact
Shahriar (@dhaka.witness)
https://steemit.com/@dhaka.witness
https://x.com/Shahriar1933
