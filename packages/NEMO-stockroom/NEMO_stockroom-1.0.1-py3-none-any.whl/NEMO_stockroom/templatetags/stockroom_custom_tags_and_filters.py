from django import template

from NEMO_stockroom.models import ConsumableThumbnail

register = template.Library()

@register.filter
def get_thumbnail_url(consumable_id):
	try:
		t = ConsumableThumbnail.objects.get(consumable_id=consumable_id)
	except:
		return ""

	return t.image.url

@register.filter
def get_total_price(unit_price, qty):
	unit_price = float(unit_price)
	qty = float(qty)
	return str(round(unit_price / qty, 2))
