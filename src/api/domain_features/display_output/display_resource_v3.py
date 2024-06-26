import requests
from flask import render_template, make_response
from flask_restful import Resource, reqparse


class DisplayImageResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'random_seed',
            type=int,
            required=True,
            help='Random seed is required',
            location='json'
        )
        self.reqparse.add_argument(
            'number_steps',
            type=int,
            required=True,
            help='Number of interpolation steps is required',
            location='json'
        )

    def get(self):
        payload = {
            'random_seed': None,
            'number_steps': 24
        }

        # Call the local generate API to fetch the image
        response = requests.post('http://localhost:8080/generate', json=payload)
        image_data = response.json()

        if image_data['success']:
            # Decode the base64 image
            print(len(image_data['generated_images']))
            # Render the HTML page with the image displayed
            html = render_template('display_generated_image_v4.html',
                                   generated_images=image_data['generated_images'])

            return make_response(html)
        else:
            return {'message': 'Failed to generate image'}, 500

    def post(self):
        args = self.reqparse.parse_args()
        random_seed = args['random_seed']
        number_steps = args['number_steps']

        # Construct the payload for the generate endpoint
        payload = {
            'random_seed': random_seed,
            'number_steps': number_steps
        }

        # Call the local generate API to fetch the image with parameters
        response = requests.post('http://localhost:8080/generate', json=payload)
        image_data = response.json()

        if image_data['success']:
            # Decode the base64 image
            # Render the HTML page with the image displayed
            html = render_template('display_generated_image_v4.html',
                                   generated_images=image_data['generated_images'])
            return make_response(html)
        else:
            return {'message': 'Failed to generate image'}, 500
