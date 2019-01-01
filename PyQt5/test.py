class Solution(object):
    def twoSum(self, nums, target):
        for index, num in enumerate(nums):
            for subindex, subnum in enumerate(nums[index + 1:]):
                if num + subnum == target:
                    return [index, subindex + index + 1]


if __name__ == "__main__":
    nums = [-1,-2,-3,-4,-5]
    print(Solution().twoSum(nums, -8))
