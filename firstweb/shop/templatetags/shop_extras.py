from django import template

register = template.Library()

CATEGORY_ICON_MAP = {
    'โน้ตบุ๊ก': 'laptop',
    'คอมพิวเตอร์ตั้งโต๊ะ': 'desktop',
    'จอภาพ': 'monitor',
    'คีย์บอร์ด': 'keyboard',
    'เมาส์': 'mouse',
    'ชุดหูฟัง': 'headset',
    'เว็บแคม': 'webcam',
    'ซีพียู': 'cpu',
    'การ์ดจอ': 'gpu',
    'เมนบอร์ด': 'motherboard',
    'หน่วยความจำ': 'memory',
    'อุปกรณ์จัดเก็บข้อมูล': 'storage',
    'พาวเวอร์ซัพพลาย': 'psu',
    'เคสคอมพิวเตอร์': 'case',
    'เครื่องสำรองไฟ': 'ups',
    'อุปกรณ์เครือข่าย': 'router',
}


@register.filter
def category_icon(category_name):
    return CATEGORY_ICON_MAP.get(category_name, 'default')
