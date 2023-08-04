def is_combination_above_threshold(numbers, threshold):
        def check_combination(index, current_sum):
            if current_sum >= threshold:
                return True
            if index >= len(numbers):
                return False

            # Include the current number in the sum
            if check_combination(index + 1, current_sum + numbers[index]):
                return True

            # Exclude the current number from the sum
            if check_combination(index + 1, current_sum):
                return True

            return False

        return check_combination(0, 0)

numbers = []
threshold = 0

result = is_combination_above_threshold(numbers, threshold)
print(result)
