from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from datetime import datetime
import logging
from django.shortcuts import render
from . import models  # Import models dynamically
from django.utils.timezone import make_aware
import pytz


logger = logging.getLogger(__name__)


def home(request):
    # simple render of home page - confirmation of successful deployment
    return render(request, "main.html")

@csrf_exempt
@require_POST
def webhook_1H(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        # Convert timestamp to timezone-aware datetime
        timestamp = make_aware(datetime.fromtimestamp(int(data['timestamp']) / 1000))

        # Password check
        if data.get("password") != "your_password_of_choice":
            return JsonResponse({'status': 'error', 'message': 'Invalid password'}, status=403)

        DATABASE_MODELS = {
            # DB table name, asset prefix from pinescript
            'BTCUSD_1H': 'btc',
            'ETHUSD_1H': 'eth',
            'SOLUSD_1H': 'sol',
            'XRPUSD_1H': 'xrp',
            'BNBUSD_1H': 'bnb',
            'SUIUSD_1H': 'sui'
        }

        results = {}
        for model_name, prefix in DATABASE_MODELS.items():
            model = getattr(models, model_name, None)
            if model is None:
                logger.error(f"Model {model_name} not found")
                continue  

            prices = {
                'open': float(data[f'{prefix}_open']),
                'high': float(data[f'{prefix}_high']),
                'low': float(data[f'{prefix}_low']),
                'close': float(data[f'{prefix}_close']),
                'volume': float(data[f'{prefix}_volume']),
            }

            try:
                obj = model.objects.create(time=timestamp, **prices)
                results[prefix] = True  
            except Exception as e:
                logger.error(f"Error creating record for {model_name}: {str(e)}")
                results[prefix] = False  

        return JsonResponse({
            'status': 'success',
            'message': f'Data for webhook 1H at {timestamp} processed successfully',
            'created': results
        }, status=200)

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON data: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
    except KeyError as e:
        logger.error(f"Missing required field: {str(e)}")
        return JsonResponse({'status': 'error', 'message': f'Missing field: {str(e)}'}, status=400)
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



# If you need more timeframes, copy the function below and change the "TIMEFRAME" for your desired timeframe
# in function name, DATABASE_MODELS and line 134 (optional)

@csrf_exempt
@require_POST
def webhook_TIMEFRAME(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        # Convert timestamp to timezone-aware datetime
        timestamp = make_aware(datetime.fromtimestamp(int(data['timestamp']) / 1000))

        # Password check
        if data.get("password") != "your_password_of_choice":
            return JsonResponse({'status': 'error', 'message': 'Invalid password'}, status=403)

        DATABASE_MODELS = {
            # DB table name, asset prefix from pinescript
            'BTCUSD_TIMEFRAME': 'btc',
            'ETHUSD_TIMEFRAME': 'eth',
            'SOLUSD_TIMEFRAME': 'sol',
            'XRPUSD_TIMEFRAME': 'xrp',
            'BNBUSD_TIMEFRAME': 'bnb',
            'SUIUSD_TIMEFRAME': 'sui',
            # Insert more records if you have more data coming through the TradingView webhook
        }

        results = {}
        for model_name, prefix in DATABASE_MODELS.items():
            model = getattr(models, model_name, None)
            if model is None:
                logger.error(f"Model {model_name} not found")
                continue  

            prices = {
                'open': float(data[f'{prefix}_open']),
                'high': float(data[f'{prefix}_high']),
                'low': float(data[f'{prefix}_low']),
                'close': float(data[f'{prefix}_close']),
                'volume': float(data[f'{prefix}_volume']),
            }

            try:
                obj = model.objects.create(time=timestamp, **prices)
                results[prefix] = True  
            except Exception as e:
                logger.error(f"Error creating record for {model_name}: {str(e)}")
                results[prefix] = False  

        return JsonResponse({
            'status': 'success',
            'message': f'Data for webhook TIMEFRAME at {timestamp} processed successfully',
            'created': results
        }, status=200)

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON data: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
    except KeyError as e:
        logger.error(f"Missing required field: {str(e)}")
        return JsonResponse({'status': 'error', 'message': f'Missing field: {str(e)}'}, status=400)
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)