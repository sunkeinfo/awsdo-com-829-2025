#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

# 定义要更新的文件列表
files_to_update = [
    'linux-server.html',
    'windows-server.html',
    'residential-ip-server.html',
    'performance-server.html'
]

# 颜色替换映射
replacements = [
    # 导航链接颜色 #007bff → #6366f1
    (r'color:\s*#007bff(?!.*rgb)', 'color: #6366f1'),
    
    # 背景色升级
    (r'background-color:\s*#f8f9fa', 'background: linear-gradient(135deg, #f8fafc 0%, #f4f7fa 100%)'),
    (r'background:\s*#f8f9fa', 'background: linear-gradient(135deg, #f8fafc 0%, #f4f7fa 100%)'),
    
    # 文字色升级
    (r'color:\s*#343a40', 'color: #1e293b'),
    
    # 卡片圆角调整 (从999px/50px到12px)
    (r'border-radius:\s*999px', 'border-radius: 12px'),
    (r'border-radius:\s*50px', 'border-radius: 12px'),
]

def upgrade_html_file(filepath):
    """升级单个HTML文件的CSS"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 替换导航链接颜色
        content = re.sub(
            r'nav a:hover, nav a\.active\s*{\s*color:\s*#007bff',
            'nav a:hover, nav a.active { color: #6366f1',
            content
        )
        
        # 升级背景色 (在 body 样式中)
        content = re.sub(
            r'(body\s*{[^}]*background-color:\s*)#f8f9fa',
            r'\1linear-gradient(135deg, #f8fafc 0%, #f4f7fa 100%)',
            content
        )
        
        # 升级文字色
        content = re.sub(
            r'(body\s*{[^}]*color:\s*)#343a40',
            r'\1#1e293b',
            content
        )
        
        # 更新卡片样式 - feature-card
        content = re.sub(
            r'\.feature-card\s*{([^}]*background:\s*#ffffff[^}]*border-radius:\s*)14px',
            r'.feature-card {\1 12px',
            content
        )
        
        # 更新阴影和边框效果
        if 'feature-card' in content:
            content = re.sub(
                r'(\.feature-card\s*{[^}]*background:\s*#ffffff[^}]*border:\s*1px solid[^}]*box-shadow:\s*)0 10px 30px rgba\(0,0,0,0\.05\)',
                r'\10 4px 30px rgba(0, 0, 0, 0.03), 0 0 20px rgba(99, 102, 241, 0.05)',
                content,
                flags=re.DOTALL
            )
        
        # 如果有修改，保存文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已更新: {filepath}")
            return True
        else:
            print(f"⚠️  无更改: {filepath}")
            return False
    except Exception as e:
        print(f"❌ 错误处理 {filepath}: {e}")
        return False

# 执行更新
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    updated_count = 0
    
    for filename in files_to_update:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            if upgrade_html_file(filepath):
                updated_count += 1
        else:
            print(f"⚠️  文件未找到: {filepath}")
    
    print(f"\n总计: 已更新 {updated_count} 个文件")
