import random
from collections import Counter

def duiduipeng(lucky_number=0, show_log=True):
    def log_print(*args, **kwargs):
        if show_log:
            print(*args, **kwargs)
    
    def has_pairs(numbers):
        # 检查列表中是否有重复的数字
        return len(numbers) != len(set(numbers))
    
    def remove_pairs(numbers):
        # 找到第一对重复的数字
        first_pair = None
        seen = set()
        for num in numbers:
            if num in seen:
                first_pair = num
                break
            seen.add(num)
        
        # 移除这一对数字
        remaining = []
        removed = []
        pair_count = 0
        for num in numbers:
            if num == first_pair and pair_count < 2:
                removed.append(num)
                pair_count += 1
            else:
                remaining.append(num)
        if show_log:
            print(f"移除一对{first_pair}，剩余数字: {remaining}")
        return remaining
    
    def count_lucky_number(numbers, lucky_number):
        # 计算幸运数字在列表中出现的次数
        return numbers.count(lucky_number)
    
    def add_random_numbers(numbers, count):
        new_numbers = numbers.copy()
        added_numbers = []
        for _ in range(count):
            new_num = random.randint(1, 9)
            added_numbers.append(new_num)
            new_numbers.append(new_num)
        log_print(f"追加的随机数字: {added_numbers}")
        log_print(f"追加后的数列: {new_numbers}")
        return new_numbers
    
    # 初始化得分
    score = 0
    # 初始化9个随机数字
    numbers = [random.randint(1, 9) for _ in range(9)]
    log_print(f"\n===== 游戏开始 =====")
    log_print(f"初始数字: {numbers}")
    
    # 如果有幸运数字，检查并添加额外的随机数字
    if lucky_number:
        # 检查初始数列中幸运数字的数量
        lucky_count = count_lucky_number(numbers, lucky_number)
        if lucky_count > 0:
            log_print(f"\n初始检测: 发现{lucky_count}个幸运数字{lucky_number}")
            numbers = add_random_numbers(numbers, lucky_count)
            # 检查新添加的数字中是否有幸运数字
            while True:
                new_lucky_count = count_lucky_number(numbers[-lucky_count:], lucky_number)
                if new_lucky_count == 0:
                    break
                log_print(f"\n追加检测: 新增数字中有{new_lucky_count}个幸运数字{lucky_number}")
                numbers = add_random_numbers(numbers, new_lucky_count)
                lucky_count = new_lucky_count
            
        log_print(f"\n初始阶段结束，最终数列: {numbers}")
    
    # 游戏主循环
    round_count = 0
    while has_pairs(numbers):
        round_count += 1
        log_print(f"\n=== 回合 {round_count} ===")
        log_print(f"当前数列: {numbers}")
        
        # 移除所有成对的数字
        numbers = remove_pairs(numbers)
        score += 1
        
        # 添加新数字
        new_num = random.randint(1, 9)
        numbers.append(new_num)
        log_print(f"添加随机数字: {new_num}")
        log_print(f"添加后数列: {numbers}")
        
        # 检查新数字是否是幸运数字
        if lucky_number and new_num == lucky_number:
            log_print(f"\n触发幸运数字: 新增了幸运数字{lucky_number}")
            numbers = add_random_numbers(numbers, 1)
            
            while numbers[-1] == lucky_number:
                log_print(f"\n连锁反应: 新增数字是幸运数字{lucky_number}")
                numbers = add_random_numbers(numbers, 1)
    
    log_print(f"\n===== 游戏结束 =====")
    log_print(f"最终数列: {numbers}")
    log_print(f"最终得分: {score}")
    return score

def print_bar_chart(distribution, total_times, bar_width=50):
    print("\n结果分布统计：")
    max_count = max(distribution.values())
    
    # 计算极端情况的概率
    zero_count = distribution.get(0, 0)
    high_count = sum(distribution[k] for k in distribution if k >= 13)
    zero_percent = (zero_count / total_times) * 100
    high_percent = (high_count / total_times) * 100
    
    print(f"\n极端情况概率：")
    print(f"得分为0的概率: {zero_percent:.2f}%")
    print(f"得分≥13的概率: {high_percent:.2f}%")
    
    print("\n详细分布：")
    for number in sorted(distribution.keys()):
        count = distribution[number]
        percentage = (count / total_times) * 100
        bar_length = int((count / max_count) * bar_width)
        bar = '█' * bar_length
        print(f" {number:2d}碰 | {bar} {count} 次 ({percentage:.2f}%)")

def main():
    try:
        base_times = int(input("请输入每种情况的执行次数: "))
        total_times = base_times * 10  # 10种情况（不奶任何角色 + 9个幸运数字）
        print(f"\n将执行总计 {total_times} 次游戏（每种情况 {base_times} 次）")
        
        # 存储所有情况的结果
        all_results = {}
        
        # 执行不奶任何角色的情况
        print("\n=== 不奶任何角色的情况 ===")
        results = []
        for _ in range(base_times):
            result = duiduipeng(lucky_number=0, show_log=False)
            results.append(result)
        distribution = Counter(results)
        print_bar_chart(distribution, base_times)
        all_results["不奶任何角色"] = distribution
        
        # 执行有幸运数字1-9的情况
        results = []
        for _ in range(base_times):
            result = duiduipeng(lucky_number=1, show_log=False)
            results.append(result)
        distribution = Counter(results)
        print_bar_chart(distribution, base_times)
        all_results[f"奶角色"] = distribution
        
        # 打印总体统计
        print("\n========== 总体统计 ==========")
        print(f"每种情况执行次数: {base_times}")
        for situation, dist in all_results.items():
            avg_score = sum(score * count for score, count in dist.items()) / base_times
            max_score = max(dist.keys())
            min_score = min(dist.keys())
            zero_count = dist.get(0, 0)
            high_count = sum(dist[k] for k in dist if k >= 13)
            zero_percent = (zero_count / base_times) * 100
            high_percent = (high_count / base_times) * 100
            
            print(f"\n{situation}:")
            print(f"平均 {avg_score:.2f} 碰")
            print(f"最高 {max_score} 碰")
            print(f"最低 {min_score} 碰")
            print(f"烫金方的概率: {zero_percent + high_percent:.2f}%")
            
    except ValueError:
        print("请输入有效的数字！")

if __name__ == "__main__":
    main()
