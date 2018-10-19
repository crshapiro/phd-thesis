import numpy as np
import matplotlib.pyplot as plt
import csv
plt.style.use('std-srf')

def get_data(file):
    with open(file, 'r') as csvfile:
        # Countries in EU
        EU_countries = ['Austria','Belgium','Bulgaria','Croatia','Cyprus','Czech Republic','Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Ireland','Italy','Latvia','Lithuania','Luxembourg','Malta','Netherlands','Poland','Portugal','Romania','Slovakia','Slovenia','Spain','Sweden','United Kingdom','Former Czechoslovakia','Germany, East','Germany, West']
        # Open file
        rd = csv.reader(csvfile)
        # Empty dict
        dat = dict()
        # Read the first row for the years
        dat['years'] = np.array(next(rd)[2:], dtype=np.float64)
        # Allocation total dateration
        dat['EU'] = np.zeros(np.size(dat['years']))
        dat['US'] = np.zeros(np.size(dat['years']))
        dat['China'] = np.zeros(np.size(dat['years']))
        dat['other'] = np.zeros(np.size(dat['years']))
        for row in rd:
            if (row[0] in EU_countries):
                dat['EU'] += np.array(row[2:], dtype=np.float64)
            elif (row[0] == 'United States'):
                dat['US'] = np.array(row[2:], dtype=np.float64)
            elif (row[0] == 'China'):
                dat['China'] = np.array(row[2:], dtype=np.float64)
            else:
                dat['other'] += np.array(row[2:], dtype=np.float64)

    return dat

# Total dateration
total = get_data('generation.csv')
wind = get_data('wind.csv')
renew = get_data('nonhydro-renewables.csv')

# Create figure
fig = plt.figure(figsize=(6.5,5))

# Plot total Renewables
ax = fig.add_subplot(2,2,1)
ax.bar(renew['years'],renew['other'],width=0.9,linewidth=0.9)
ax.bar(renew['years'],renew['China'],bottom = renew['other'],width=0.9,linewidth=0.9)
ax.bar(renew['years'],renew['US'],bottom = renew['other'] + renew['China'],width=0.9,linewidth=0.9)
ax.bar(renew['years'],renew['EU'],bottom = renew['other'] + renew['China'] + renew['US'],width=0.9,linewidth=0.9)
ax.set_xticks(np.arange(1980,2020,5))
ax.xaxis.set_tick_params(rotation=45)
ax.set_xlim([1979.5,2015.5])
ax.set_title('Renewables (Non-hydro)')
ax.set_ylabel('Generation (TWh)')

# Plot Wind
ax = fig.add_subplot(2,2,2)
ax.bar(wind['years'],wind['other'],width=0.9)
ax.bar(wind['years'],wind['China'],bottom = wind['other'],width=0.9)
ax.bar(wind['years'],wind['US'],bottom = wind['other'] + wind['China'],width=0.9)
ax.bar(wind['years'],wind['EU'],bottom = wind['other'] + wind['China'] + wind['US'],width=0.9)
ax.set_xticks(np.arange(1980,2020,5))
ax.set_xlim([1979.5,2015.5])
ax.xaxis.set_tick_params(rotation=45)
ax.set_title('Wind')
ax.set_ylabel('Generation (TWh)')
# ax.set_ylabel('GWh')

# Plot total Renewables
ax = fig.add_subplot(2,2,3)
ind = total['years']>=renew['years'][0]
ax.plot(renew['years'],renew['other']/total['other'][ind]*100)
ax.plot(renew['years'],renew['China']/total['China'][ind]*100)
ax.plot(renew['years'],renew['US']/total['US'][ind]*100)
ax.plot(renew['years'],renew['EU']/total['EU'][ind]*100)
# ax.bar(renew['years'],renew['China'],bottom = renew['other'])
# ax.bar(renew['years'],renew['US'],bottom = renew['other'] + renew['China'])
# ax.bar(renew['years'],renew['EU'],bottom = renew['other'] + renew['China'] + renew['US'])
ax.set_xticks(np.arange(1980,2020,5))
ax.xaxis.set_tick_params(rotation=45)
ax.set_xlim([1979.5,2015.5])
ax.set_ylabel('% of total generation')

# Plot total windables
ax = fig.add_subplot(2,2,4)
ind = total['years']>=wind['years'][0]
ax.plot(wind['years'],wind['other']/total['other'][ind]*100)
ax.plot(wind['years'],wind['China']/total['China'][ind]*100)
ax.plot(wind['years'],wind['US']/total['US'][ind]*100)
ax.plot(wind['years'],wind['EU']/total['EU'][ind]*100)
# ax.bar(renew['years'],renew['China'],bottom = renew['other'])
# ax.bar(renew['years'],renew['US'],bottom = renew['other'] + renew['China'])
# ax.bar(renew['years'],renew['EU'],bottom = renew['other'] + renew['China'] + renew['US'])
ax.set_xticks(np.arange(1980,2020,5))
ax.xaxis.set_tick_params(rotation=45)
ax.set_xlim([1979.5,2015.5])
ax.set_ylabel('% of total generation')

print(wind['other'][-3]/total['other'][-3]*100.0)
print(wind['China'][-3]/total['China'][-3]*100.0)
print(wind['US'][-3]/total['US'][-3]*100.0)
print(wind['EU'][-3]/total['EU'][-3]*100.0)

plt.tight_layout()
plt.savefig('gen-hist.pdf')
