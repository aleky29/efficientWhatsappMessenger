import re
from collections import Counter, defaultdict
from datetime import datetime

import matplotlib.pyplot as plt

# Replace with your WhatsApp chat export file path
CHAT_FILE = 'chat.txt'
# Regex pattern for WhatsApp message lines (adjust if your format is different)

# Adjusted regex for new format: [5/10/24, 22:15:29] Name: Message
MESSAGE_PATTERN = re.compile(r'^\[(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}):\d{2}\] ([^:]+):')

def parse_chat(file_path):
    activity = defaultdict(list)  # {friend: [(weekday, hour), ...]}
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            match = MESSAGE_PATTERN.match(line)
            if match:
                date_str, time_str, sender = match.groups()
                # Try both d/m/y and m/d/y
                for fmt in ("%d/%m/%y %H:%M", "%m/%d/%y %H:%M", "%d/%m/%Y %H:%M", "%m/%d/%Y %H:%M"):
                    try:
                        dt = datetime.strptime(f"{date_str} {time_str}", fmt)
                        break
                    except ValueError:
                        dt = None
                if not dt:
                    continue
                weekday = dt.strftime('%A')
                hour = dt.hour
                activity[sender].append((weekday, hour))
    return activity

def analyze_activity(activity):
    results = {}
    for friend, times in activity.items():
        counter = Counter(times)
        top = counter.most_common(5)
        results[friend] = top
    return results

def print_results(results):

    for friend, top_times in results.items():
        print(f"\nTop active times for {friend}:")
        for i, ((weekday, hour), count) in enumerate(top_times, 1):
            print(f"{i}. {weekday} {hour:02d}:00 ({count} messages)")

if __name__ == "__main__":
    activity = parse_chat(CHAT_FILE)
    results = analyze_activity(activity)
    print_results(results)
    # To plot for a specific friend, uncomment and set the name:
    #plotting for all friends, writing the actual value for the max and min values in the heatmap corresponding square
    for friend in activity.keys():
        #plotting for all friends, writing the actual value for the max and min values in the heatmap corresponding square
        #since we already have the heatmap with numbers, no need to plot the one without numbers
        heatmap = [[0]*24 for _ in range(7)]
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for weekday, hour in activity[friend]:
            day_idx = days.index(weekday)
            heatmap[day_idx][hour] += 1
        plt.figure(figsize=(12, 5))
        plt.imshow(heatmap, aspect='auto', cmap='YlGnBu')
        plt.yticks(range(7), days)
        plt.xticks(range(24), [f"{h:02d}:00" for h in range(24)], rotation=45)
        plt.colorbar(label='Messages')
        plt.title(f"Activity Heatmap for {friend}")
        plt.xlabel("Hour of Day")
        plt.ylabel("Day of Week")
        plt.tight_layout()
        for i in range(7):
            for j in range(24):
                color = 'white' if heatmap[i][j] >= (max(map(max, heatmap)) / 2) else 'black'
                plt.text(j, i, heatmap[i][j], ha='center', va='center', color=color)
        plt.show()
        # Uncomment the next line to save the heatmap as an image
        # plt.savefig(f"{friend}_heatmap.png")
        plt.close()
 
