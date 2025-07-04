import os
import pandas as pd
from flask import Flask, render_template, request
from kafka import KafkaProducer
import json
from helper.logger import logger
from helper.helper import file_validator

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

producer = KafkaProducer(
    bootstrap_servers=os.getenv('KAFKA_BROKER'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')

        # Check if the file exists and is a valid CSV
        if file and file_validator(file.filename):
           
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            try:
                df = pd.read_csv(filepath, sep=',')
        
                df = df.sort_values(by=df.columns[:2].tolist())        

                df_unique = df.drop_duplicates()

                #duplicated
                duplicated_rows = df[df.duplicated(keep=False)]
                duplicated_list = duplicated_rows.to_dict(orient='records') if not duplicated_rows.empty else None

                #suspicious
                suspect_records = df_unique[df_unique['amount'] > 8000]
                suspect_list = suspect_records.to_dict(orient='records') if not suspect_records.empty else None

                for _, row in df_unique.iterrows():
                    producer.send(os.getenv('KAFKA_TOPIC'), row.to_dict())
                producer.flush()

                if duplicated_list and suspect_list:
                    return render_template(
                        'index.html',
                        message="CSV uploaded and sent to Kafka successfully! Duplicated rows and suspect records found.",
                        duplicated_rows=duplicated_list,
                        suspect_rows=suspect_list
                    )
                elif duplicated_list:
                    return render_template(
                        'index.html',
                        message="CSV uploaded and sent to Kafka successfully! Duplicated rows found.",
                        duplicated_rows=duplicated_list,
                        suspect_rows=None
                    )
                elif suspect_list:
                    return render_template(
                        'index.html',
                        message="CSV uploaded and sent to Kafka successfully! Suspect records found.",
                        duplicated_rows=None,
                        suspect_rows=suspect_list
                    )
                else:
                    return render_template(
                        'index.html',
                        message="CSV uploaded and sent to Kafka successfully! No duplicated rows or suspect records found.",
                        duplicated_rows=None,
                        suspect_rows=None
                    )
            except Exception as e:
                logger.error(f"Error parsing CSV: {str(e)}")
                return render_template('index.html', message=f"Error parsing CSV: {str(e)}")
        else:
            logger.warning("Invalid file. Please upload a CSV file.")
            return render_template('index.html', message="Invalid file. Please upload a CSV file.")
    return render_template('index.html', message=None)

if __name__ == '__main__':
    app.run(debug=True, host=os.getenv("UI_HOST"), port=os.getenv("UI_PORT"))
