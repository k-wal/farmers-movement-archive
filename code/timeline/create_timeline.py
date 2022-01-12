import matplotlib.pyplot as plt
import datetime
import numpy as np
from datetime import timedelta

def read_events():
	file = open('events.txt', 'r')
	lines = file.readlines()
	file.close()
	
	dates = []
	labels = []
	for line in lines:
		line = line.strip().split('||')
		date, label = line[0], line[1]
		date = datetime.datetime.strptime(date, "%d-%m-%Y")
		dates.append(date)
		labels.append(label)

	return dates, labels

def show_timeline(dates, labels):
	min_date = datetime.date(np.min(dates).year, np.min(dates).month, np.min(dates).day) - timedelta(days=30)
	max_date = datetime.date(np.max(dates).year, np.max(dates).month, np.max(dates).day) + timedelta(days=30)
	 
	# labels with associated dates
	# labels = ['{0:%d %b %Y}:\n{1}'.format(d, l) for l, d in zip (labels, dates)]	
	labels = ['{0}, {1:%d %b %Y}|{1:%d %b %Y}, {0}'.format(l,d) for l, d in zip (labels, dates)]	

	fig, ax = plt.subplots(figsize=(6, 10), constrained_layout=True)
	_ = ax.set_xlim(-20, 20)
	_ = ax.set_ylim(min_date, max_date)
	_ = ax.axvline(0, ymin=0.00, ymax=1, c='deeppink', zorder=1)
	 
	_ = ax.scatter(np.zeros(len(dates)), dates, s=120, c='palevioletred', zorder=2)
	_ = ax.scatter(np.zeros(len(dates)), dates, s=30, c='darkmagenta', zorder=3)

	fontsize = 11

	label_offsets = np.repeat(2.1, len(dates))
	label_offsets[1::2] = -2.1
	for i, (l, d) in enumerate(zip(labels, dates)):
		d = d - timedelta(days=3)
		align = 'right'
		if i % 2 == 0:
			align = 'left'
			l = l.split('|')[1]
			_ = ax.text(label_offsets[i], d, l.split(',')[0], ha=align, fontfamily='comic-sans', fontweight='bold', color='red', fontsize=fontsize)
			l = l.split(',')[1]
			label_offsets[i] += 2.3
		else:
			l = l.split('|')[0]
			_ = ax.text(label_offsets[i], d, l.split(',')[1], ha=align, fontfamily='comic-sans', fontweight='bold', color='red', fontsize=fontsize)
			l = l.split(',')[0]
			label_offsets[i] -= 2.3
		_ = ax.text(label_offsets[i], d, l, ha=align, fontfamily='comic-sans', fontweight='bold', color='green',fontsize=fontsize)	

	stems = np.repeat(2.0, len(dates))
	stems[1::2] *= -1.0   
	x = ax.hlines(dates, 0, stems, color='darkmagenta')	

	# hide lines around chart
	for spine in ["left", "top", "right", "bottom"]:
		_ = ax.spines[spine].set_visible(False)
	 
	# hide tick labels
	_ = ax.set_xticks([])
	_ = ax.set_yticks([])
	 
	_ = ax.set_title("Farmers' Movement Archive: a timeline", fontweight="bold", fontfamily='mono', fontsize="16", color='darkblue')	

	plt.show()

def main():
	dates, labels = read_events()
	show_timeline(dates, labels)

main()