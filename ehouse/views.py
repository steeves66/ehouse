from django.shortcuts import render
from django.views import View


class HomeView(View):
	def get(self, request, *args, **kwargs):
		# products = Product.objects.all().filter(is_available=True)

		# context = {
		#     'products': products,
		# }
		return render(request, 'home.html')