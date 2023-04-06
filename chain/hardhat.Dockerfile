FROM apeworx/ape

USER root
RUN apt update
RUN apt -y upgrade
RUN apt install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt install -y nodejs


RUN npm install --global yarn
RUN pip install ape-hardhat

COPY . .
RUN npm install
RUN yarn add hardhat

ENTRYPOINT ["npx", "hardhat", "node"]