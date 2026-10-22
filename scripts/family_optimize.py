"""
麦麦遛娃点餐师 - 家庭点餐组合计算引擎
输入：menu.json / coupons.json / family_ctx.json
输出：3套最优方案 JSON
"""

from dataclasses import dataclass, field
from typing import List, Optional
import json


@dataclass
class MenuItem:
    name: str
    price: float
    category: str  # 主食/配餐/饮品/甜品/乐园餐
    calories: Optional[int] = None
    protein: Optional[float] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class Coupon:
    coupon_id: str
    coupon_type: str  # 满减/折扣/品类券
    threshold: float = 0.0
    discount_value: float = 0.0
    applicable_categories: List[str] = field(default_factory=list)


@dataclass
class FamilyCtx:
    adult: int = 2
    kid: int = 1
    budget: float = 70.0
    no_spicy: bool = False
    low_sweet: bool = False
    must_have_kids_meal: bool = True
    swap_drink_to_milk: bool = False


@dataclass
class Scheme:
    tag: str
    items: List[str]
    original_price: float
    final_price: float
    note: str


def enumerate_schemes(menu: List[MenuItem], coupons: List[Coupon], ctx: FamilyCtx) -> List[Scheme]:
    """
    枚举家庭点餐组合，返回3套方案：
    1. 全家稳 - 均衡搭配命中满减
    2. 孩子开心 - 乐园餐优先
    3. 家长友好 - 低卡导向
    """
    schemes = []

    # 筛选商品
    mains = [m for m in menu if m.category == "主食"]
    sides = [m for m in menu if m.category == "配餐"]
    drinks = [m for m in menu if m.category == "饮品"]
    desserts = [m for m in menu if m.category == "甜品"]
    kids_meals = [m for m in menu if m.category == "乐园餐"]

    # 过滤忌口
    if ctx.no_spicy:
        mains = [m for m in mains if "辣" not in m.name and "spicy" not in m.tags]

    # 方案1：全家稳
    best_coupon = find_best_coupon(menu, coupons, ctx.budget)
    scheme1_items = []
    scheme1_price = 0.0

    for _ in range(ctx.adult):
        if mains:
            scheme1_items.append(mains[0].name)
            scheme1_price += mains[0].price

    if ctx.must_have_kids_meal and kids_meals:
        scheme1_items.append(kids_meals[0].name)
        scheme1_price += kids_meals[0].price

    scheme1_final = apply_coupon(scheme1_price, best_coupon)

    schemes.append(Scheme(
        tag="全家稳",
        items=scheme1_items,
        original_price=scheme1_price,
        final_price=scheme1_final,
        note="均衡搭配，命中满减"
    ))

    # 方案2：孩子开心
    scheme2_items = []
    scheme2_price = 0.0

    if ctx.adult >= 2 and len(mains) >= 2:
        scheme2_items.append(mains[0].name)
        scheme2_price += mains[0].price
        scheme2_items.append(mains[1].name if len(mains) > 1 else mains[0].name)
        scheme2_price += mains[1].price if len(mains) > 1 else mains[0].price

    if kids_meals:
        scheme2_items.append(kids_meals[0].name)
        scheme2_price += kids_meals[0].price

    scheme2_final = apply_coupon(scheme2_price, best_coupon)

    schemes.append(Scheme(
        tag="孩子开心",
        items=scheme2_items,
        original_price=scheme2_price,
        final_price=scheme2_final,
        note="乐园餐优先，孩子满足"
    ))

    # 方案3：家长友好（低卡）
    scheme3_items = []
    scheme3_price = 0.0

    # 选低卡主食
    low_cal_mains = sorted(mains, key=lambda m: m.calories or 999)
    for i in range(ctx.adult):
        if i < len(low_cal_mains):
            scheme3_items.append(low_cal_mains[i].name)
            scheme3_price += low_cal_mains[i].price

    if ctx.must_have_kids_meal and kids_meals:
        scheme3_items.append(kids_meals[0].name)
        scheme3_price += kids_meals[0].price

    # 换低卡配餐
    if sides:
        low_cal_side = min(sides, key=lambda s: s.calories or 999)
        scheme3_items.append(low_cal_side.name)
        scheme3_price += low_cal_side.price

    scheme3_final = apply_coupon(scheme3_price, best_coupon)

    schemes.append(Scheme(
        tag="家长友好",
        items=scheme3_items,
        original_price=scheme3_price,
        final_price=scheme3_final,
        note="低卡导向，整体更健康"
    ))

    return schemes


def find_best_coupon(menu: List[MenuItem], coupons: List[Coupon], budget: float) -> Optional[Coupon]:
    """找最优满减券"""
    best = None
    best_discount = 0.0

    for coupon in coupons:
        if coupon.coupon_type == "满减" and coupon.threshold <= budget:
            if coupon.discount_value > best_discount:
                best_discount = coupon.discount_value
                best = coupon

    return best


def apply_coupon(total: float, coupon: Optional[Coupon]) -> float:
    """应用优惠券"""
    if not coupon:
        return total

    if coupon.coupon_type == "满减" and total >= coupon.threshold:
        return total - coupon.discount_value

    return total


def output_json(schemes: List[Scheme]) -> str:
    """输出JSON格式结果"""
    result = {
        "schemes": [
            {
                "tag": s.tag,
                "items": s.items,
                "original_price": s.original_price,
                "final_price": s.final_price,
                "note": s.note
            }
            for s in schemes
        ]
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 示例
    sample_menu = [
        MenuItem("板烧鸡腿堡", 22.0, "主食", 480, 25.0, []),
        MenuItem("麦辣鸡腿堡", 20.0, "主食", 520, 23.0, ["辣"]),
        MenuItem("双层吉士", 24.0, "主食", 560, 28.0, []),
        MenuItem("薯条(中)", 11.0, "配餐", 320, 4.0, []),
        MenuItem("玉米杯", 7.0, "配餐", 120, 3.0, []),
        MenuItem("零度可乐", 5.0, "饮品", 0, 0, []),
        MenuItem("鲜煮奶", 8.0, "饮品", 150, 6.0, []),
        MenuItem("开心乐园餐", 18.0, "乐园餐", 400, 12.0, []),
    ]

    sample_coupons = [
        Coupon("c1", "满减", 60.0, 8.0, []),
        Coupon("c2", "满减", 30.0, 5.0, []),
    ]

    ctx = FamilyCtx(adult=2, kid=1, budget=70.0, no_spicy=False, low_sweet=False, must_have_kids_meal=True)

    schemes = enumerate_schemes(sample_menu, sample_coupons, ctx)
    print(output_json(schemes))
