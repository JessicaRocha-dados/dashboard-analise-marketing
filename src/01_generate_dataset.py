# /src/01_generate_dataset.py
# Objetivo: Gerar um dataset sintético, realista e REPRODUTÍVEL para a análise.

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Fixa a semente aleatória para garantir reprodutibilidade
np.random.seed(42)
random.seed(42)

print("Iniciando a geração do dataset controlado e reprodutível...")

NUM_CAMPAIGNS = 50
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)

# Definição controlada de canais para garantir consistência
campaign_channels = ['Anúncios Pagos'] * 18 + \
    ['Mídias Sociais'] * 22 + ['Email'] * 10
random.shuffle(campaign_channels)

ad_groups_map = {
    'Email': ['Boas_Vindas', 'Aniversariantes', 'Carrinho_Abandonado', 'Newsletter_Promocional'],
    'Mídias Sociais': ['Stories_Promocao', 'Influencer_Parceria', 'Feed_Novidades', 'Live_Shopping'],
    'Anúncios Pagos': ['Video_Reels', 'Search_Marca', 'Display_Retargeting', 'Shopping_Ads']
}
devices = ['Mobile', 'Desktop']
regions = ['Sudeste', 'Nordeste', 'Sul', 'Nacional', 'Centro-Oeste']

data = []
for i, channel in enumerate(campaign_channels):
    campaign_id = f'CAMP{str(i + 1).zfill(3)}'
    if channel == 'Email':
        budget = round(random.uniform(400, 900), 2)
        impressions = int(budget * random.uniform(150, 250))
        ctr = random.uniform(0.035, 0.06)
        clicks = int(impressions * ctr)
        conversion_rate = random.uniform(0.05, 0.08)
        conversions = int(clicks * conversion_rate)
    elif channel == 'Mídias Sociais':
        budget = round(random.uniform(1000, 3000), 2)
        impressions = int(budget * random.uniform(200, 300))
        ctr = random.uniform(0.025, 0.045)
        clicks = int(impressions * ctr)
        conversion_rate = random.uniform(0.02, 0.035)
        conversions = int(clicks * conversion_rate)
    else:
        budget = round(random.uniform(3500, 8000), 2)
        impressions = int(budget * random.uniform(250, 350))
        ctr = random.uniform(0.015, 0.03)
        clicks = int(impressions * ctr)
        conversion_rate = random.uniform(0.018, 0.025)
        conversions = int(clicks * conversion_rate)
    start_date = START_DATE + \
        timedelta(days=random.randint(0, (END_DATE - START_DATE).days - 30))
    end_date = start_date + timedelta(days=random.randint(7, 45))
    ad_group = random.choice(ad_groups_map[channel])
    device = random.choice(devices)
    region = random.choice(regions)
    impressions = int(impressions * random.uniform(0.9, 1.1))
    clicks = int(clicks * random.uniform(0.85, 1.15))
    conversions = int(conversions * random.uniform(0.8, 1.2))
    data.append([campaign_id, channel, start_date.strftime('%Y-%m-%d'), end_date.strftime(
        '%Y-%m-%d'), budget, impressions, clicks, conversions, ad_group, device, region])

columns = ['CampaignID', 'Channel', 'StartDate', 'EndDate', 'Budget_BRL',
           'Impressions', 'Clicks', 'Conversions', 'Ad_Group', 'Device', 'Region']
df = pd.DataFrame(data, columns=columns)

nan_indices = df.sample(frac=0.1, random_state=42).index
df.loc[nan_indices, 'Conversions'] = np.nan
df.loc[df.index == 5, ['Budget_BRL', 'Clicks', 'Conversions']] = [
    9500.00, 15000, 150]
df.loc[df.index == 25, ['Budget_BRL', 'Conversions']] = [300.00, 400]
valor_calculado = df.loc[df.index == 45, 'Impressions'] * 0.15
df.loc[df.index == 45, 'Clicks'] = int(valor_calculado.iloc[0])
df['Conversions'] = df['Conversions'].astype('Int64')

script_dir = os.path.dirname(__file__)
project_root = os.path.dirname(script_dir)
output_path = os.path.join(
    project_root, 'data', '01_raw', 'marketing_campaign_performance.csv')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)

print(f"Dataset controlado e consistente salvo com sucesso em: {output_path}")
