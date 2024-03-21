from django.shortcuts import render
from .forms import ScrapingForm
import requests, re
from bs4 import BeautifulSoup
import time


def scrappview(request):
    if request.method == 'POST':
        form = ScrapingForm(request.POST)
        if form.is_valid():
            base_url = form.cleaned_data['url_to_scrape']
            class_names = form.cleaned_data['class_names'].split()
            max_pages = form.cleaned_data.get('max_pages', 300)  # Utiliser 300 comme valeur par défaut si max_pages n'est pas défini

            match = re.search(r'\{(\d+)\}', base_url)
            number = int(match.group(1)) if match else 1

            scraped_data = []
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://jpocci12.fr/',
                # Ajoutez d'autres en-têtes si nécessaire
            }

            while number <= max_pages:
                current_url = re.sub(r'\{.*?\}', str(number), base_url, count=1)
                response = requests.get(current_url, headers=headers)
                print('Scraping', current_url, "response", response.status_code)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for class_name in class_names:
                        elements = soup.find_all(class_=class_name)
                        for element in elements:
                            text = element.get_text(strip=True)
                            if text:
                                scraped_data.append(text)
                    number += 1
                else:
                    break

            return render(request, 'scraping_results.html', {'scraped_data': scraped_data})

    else:
        form = ScrapingForm()
        return render(request, 'scraping_form.html', {'form': form})
