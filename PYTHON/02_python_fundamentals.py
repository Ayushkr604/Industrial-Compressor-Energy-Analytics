```python
# Industrial Compressor Energy Analytics
# Python Fundamentals

# 1. Variables and data types
compressor_id = "CP-05"
power_kw = 27.06
current_a = 52.82
running = True
reading_count = 2166

print("Compressor:", compressor_id)
print("Average power:", power_kw, "kW")
print("Average current:", current_a, "A")
print("Is running:", running)
print("Number of readings:", reading_count)

print(type(compressor_id))
print(type(power_kw))
print(type(running))
print(type(reading_count))


# 2. Lists
compressors = ["CP-01", "CP-02", "CP-03", "CP-04", "CP-05"]

print(compressors)
print("First compressor:", compressors[0])
print("Last compressor:", compressors[-1])
print("Total compressors:", len(compressors))


# 3. Loops
for compressor in compressors:
    print("Analysing:", compressor)


# 4. Conditions
power_kw = 27.06

if power_kw > 25:
    print("High power consumption")
elif power_kw > 22:
    print("Moderate power consumption")
else:
    print("Low power consumption")


# 5. Dictionaries
compressor = {
    "id": "CP-05",
    "average_power": 27.06,
    "average_current": 52.82,
    "average_flow": 372.59
}

print(compressor["id"])
print(compressor["average_power"])


# 6. Functions
def classify_power(power):
    if power > 25:
        return "High"
    elif power > 22:
        return "Moderate"
    else:
        return "Low"


print(classify_power(27.06))
print(classify_power(23.57))
print(classify_power(20.58))


for compressor in compressors:
    print("Analysing:", compressor)

for compressor in compressors:
    print("Analysing:", compressor)

power_kw = 27.06