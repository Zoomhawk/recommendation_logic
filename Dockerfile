FROM nikolaik/python-nodejs

WORKDIR /home

COPY dimension.csv .
COPY firebase.js .
COPY index.js .
COPY logic.py .
COPY model.csv .
COPY package.json .
COPY requirements.txt .

RUN npm install
RUN pip install -r requirements.txt

EXPOSE 3080

CMD ["node", "index.js"]