FROM python

WORKDIR /user_similarity_near_calculator

COPY . .

RUN pip install -r requirements.txt

workdir ../

CMD ["python3", "-m", "user_similarity_near_calculator"]
