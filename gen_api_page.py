#!/usr/bin/env python3
"""Generate api-tokens.html from models_data.txt and performance-server.html template style."""

import json

# Read models
tiers = {'free': [], 'basic': [], 'pro': [], 'premium': []}

with open('models_data.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split('|')
        if len(parts) < 5:
            continue
        model_id = parts[0]
        provider = parts[1]
        try:
            input_price = float(parts[2])
        except:
            continue
        try:
            output_price = float(parts[3])
        except:
            output_price = 0
        ctx = parts[4]

        entry = {
            'id': model_id,
            'provider': provider,
            'input': input_price,
            'output': output_price,
            'ctx': ctx
        }

        if input_price <= 0.07:
            tiers['free'].append(entry)
        elif input_price <= 1.0:
            tiers['basic'].append(entry)
        elif input_price <= 2.9:
            tiers['pro'].append(entry)
        else:
            tiers['premium'].append(entry)

# Sort each tier by input price
for k in tiers:
    tiers[k].sort(key=lambda x: (x['input'], x['id']))

# Build all models JSON for client-side search/filter
all_models = []
for tier, models in [('free', tiers['free']), ('basic', tiers['basic']), ('pro', tiers['pro']), ('premium', tiers['premium'])]:
    for m in models:
        all_models.append({
            'id': m['id'],
            'provider': m['provider'],
            'input': m['input'],
            'output': m['output'],
            'ctx': m['ctx'],
            'tier': tier
        })

models_json = json.dumps(all_models, ensure_ascii=False)

free_count = len(tiers['free'])
basic_count = len(tiers['basic'])
pro_count = len(tiers['pro'])
premium_count = len(tiers['premium'])

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI API Token Plans — AWSDO.COM</title>

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-0SXZXT6FBM"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-0SXZXT6FBM');
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6; margin: 0; padding: 0;
            background: linear-gradient(135deg, #f8fafc 0%, #f4f7fa 100%);
            color: #1e293b;
        }}
        .container {{ width: 90%; max-width: 1300px; margin: auto; overflow: hidden; }}
        header {{
            background: #ffffff; padding: 12px 0;
            border-bottom: 1px solid #e9ecef;
            position: sticky; top: 0; z-index: 1000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        header .header-inner {{ display: flex; align-items: center; gap: 24px; justify-content: space-between; }}
        header .logo {{ flex-shrink: 0; }}
        header .logo img {{ height: 44px; width: auto; display: block; }}
        nav ul {{ padding: 0; list-style: none; margin: 0; display: flex; flex-wrap: wrap; align-items: center; gap: 4px; }}
        nav ul li {{ display: inline; margin: 0 10px; }}
        nav a {{ color: #495057; text-decoration: none; font-size: 15px; font-weight: 500; transition: color 0.3s ease; white-space: nowrap; }}
        nav a:hover, nav a.active {{ color: #007bff; }}

        /* Hero */
        .hero {{
            background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #312e81 100%);
            color: #fff; padding: 70px 0 60px; position: relative; overflow: hidden;
        }}
        .hero::before {{
            content: ''; position: absolute; top: -50%; right: -20%; width: 600px; height: 600px;
            background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%); pointer-events: none;
        }}
        .hero-inner {{ display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 40px; align-items: center; }}
        .hero h1 {{ font-size: 40px; margin: 0 0 14px; font-weight: 800; line-height: 1.2; }}
        .hero h1 span {{ background: linear-gradient(90deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .hero p {{ font-size: 18px; font-weight: 300; margin: 0 0 20px; color: rgba(255,255,255,0.85); max-width: 600px; }}
        .hero-badges {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .badge {{ background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2); color: #fff; padding: 8px 14px; border-radius: 999px; font-weight: 600; font-size: 13px; display: inline-flex; align-items: center; gap: 6px; }}
        .hero-visual {{ background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); border-radius: 16px; padding: 24px; }}
        .hero-stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
        .hero-stat {{ background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 12px; padding: 18px 14px; text-align: center; }}
        .hero-stat .stat-value {{ font-size: 30px; font-weight: 800; color: #fff; line-height: 1; }}
        .hero-stat .stat-value span {{ font-size: 14px; font-weight: 600; }}
        .hero-stat .stat-label {{ font-size: 12px; color: rgba(255,255,255,0.7); margin-top: 6px; }}

        .section {{ padding: 56px 0; }}
        .section-title {{ text-align: center; margin-bottom: 14px; font-size: 32px; color: #1e293b; font-weight: 700; }}
        .section-subtitle {{ text-align: center; max-width: 820px; margin: 0 auto 42px; color: #6c757d; font-size: 16px; }}

        /* How it works */
        .steps-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }}
        @media (max-width: 900px) {{ .steps-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        @media (max-width: 520px) {{ .steps-grid {{ grid-template-columns: 1fr; }} }}
        .step-card {{ background: #fff; border-radius: 14px; padding: 24px 18px; text-align: center; box-shadow: 0 4px 16px rgba(0,0,0,0.04); border: 1px solid #eef1f4; }}
        .step-card .step-num {{ width: 40px; height: 40px; background: linear-gradient(135deg, #3b82f6, #6366f1); color: #fff; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 800; font-size: 18px; margin-bottom: 12px; }}
        .step-card h4 {{ margin: 0 0 6px; font-size: 16px; color: #1e293b; }}
        .step-card p {{ margin: 0; font-size: 13px; color: #64748b; }}

        /* Plans */
        .plans-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 36px; }}
        @media (max-width: 1100px) {{ .plans-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        @media (max-width: 600px) {{ .plans-grid {{ grid-template-columns: 1fr; }} }}
        .plan-card {{
            background: #fff; border: 2px solid #e2e8f0; border-radius: 16px;
            padding: 28px 22px; text-align: center; transition: all 0.25s;
            cursor: pointer; position: relative; overflow: hidden;
        }}
        .plan-card:hover {{ transform: translateY(-4px); box-shadow: 0 12px 36px rgba(0,0,0,0.1); }}
        .plan-card.selected {{ border-color: #3b82f6; box-shadow: 0 8px 32px rgba(59,130,246,0.18); }}
        .plan-card input[type="radio"] {{ position: absolute; top: 14px; right: 14px; accent-color: #3b82f6; width: 18px; height: 18px; }}
        .plan-card .plan-icon {{ font-size: 42px; margin-bottom: 8px; }}
        .plan-card h3 {{ margin: 0 0 4px; font-size: 20px; font-weight: 700; }}
        .plan-card .plan-price {{ font-size: 15px; font-weight: 600; color: #16a34a; margin: 8px 0; }}
        .plan-card .plan-desc {{ font-size: 13px; color: #64748b; margin: 6px 0 12px; line-height: 1.5; }}
        .plan-card .plan-range {{ display: inline-block; background: #f1f5f9; padding: 4px 12px; border-radius: 20px; font-size: 12px; color: #475569; font-weight: 500; }}
        .plan-card .model-count {{ font-size: 26px; font-weight: 800; color: #3b82f6; margin: 10px 0 2px; }}
        .plan-card .model-count-label {{ font-size: 12px; color: #94a3b8; }}
        .plan-free {{ border-color: #d1fae5; }}
        .plan-free h3 {{ color: #059669; }}
        .plan-basic {{ border-color: #dbeafe; }}
        .plan-basic h3 {{ color: #2563eb; }}
        .plan-pro {{ border-color: #e9d5ff; }}
        .plan-pro h3 {{ color: #7c3aed; }}
        .plan-premium {{ border-color: #fde68a; }}
        .plan-premium h3 {{ color: #d97706; }}
        .plan-popular {{ position: absolute; top: 0; left: 0; right: 0; background: linear-gradient(90deg, #7c3aed, #6366f1); color: #fff; font-size: 11px; font-weight: 700; padding: 4px 0; text-transform: uppercase; letter-spacing: 0.05em; }}

        /* Recharge */
        .recharge-grid {{ display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin: 20px 0; }}
        .recharge-option {{ background: #fff; border: 2px solid #e2e8f0; border-radius: 12px; padding: 16px 24px; text-align: center; cursor: pointer; transition: all 0.2s; min-width: 140px; }}
        .recharge-option:hover {{ border-color: #3b82f6; background: #eff6ff; }}
        .recharge-option.selected {{ border-color: #3b82f6; background: linear-gradient(135deg, #eff6ff, #fff); box-shadow: 0 4px 16px rgba(59,130,246,0.12); }}
        .recharge-option input[type="radio"] {{ display: none; }}
        .recharge-option .amount {{ font-size: 22px; font-weight: 800; color: #1e293b; }}
        .recharge-option .bonus {{ font-size: 13px; color: #16a34a; font-weight: 600; margin-top: 4px; }}
        .recharge-option .total {{ font-size: 12px; color: #64748b; margin-top: 2px; }}

        /* Order form */
        .form-section {{
            background: #fff; padding: 44px 40px; border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.07); border: 1px solid #eef1f4;
            max-width: 900px; margin: 0 auto;
        }}
        .form-step {{ margin-bottom: 30px; }}
        .form-step h3 {{ font-size: 20px; color: #3b82f6; display: flex; align-items: center; gap: 10px; margin: 0 0 16px; }}
        .step-icon {{ width: 34px; height: 34px; border-radius: 50%; background: #3b82f6; color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 15px; flex-shrink: 0; }}
        .section-note {{ margin: 0 0 14px; color: #6c757d; font-size: 14px; }}
        .form-group {{ margin-bottom: 18px; }}
        .form-group label {{ display: block; font-weight: 500; margin-bottom: 8px; color: #374151; font-size: 14px; }}
        .form-group input[type="text"], .form-group input[type="email"] {{
            width: 100%; padding: 12px 14px; border: 1px solid #e0e4ea; border-radius: 10px;
            font-size: 15px; font-family: 'Inter', sans-serif;
            background: #fafbfc; color: #2d3748; transition: border-color 0.15s;
        }}
        .form-group input:focus {{ outline: none; border-color: #3b82f6; background: #fff; }}
        .order-summary {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px 20px; margin: 16px 0; font-size: 14px; }}
        .order-summary .row {{ display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f1f5f9; }}
        .order-summary .row:last-child {{ border-bottom: none; }}
        .order-summary .row .label {{ color: #64748b; }}
        .order-summary .row .value {{ font-weight: 600; color: #1e293b; }}
        .order-summary .row.total .value {{ color: #059669; font-size: 18px; }}
        .submit-button {{
            display: flex; align-items: center; justify-content: center; gap: 10px;
            width: 100%; background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
            color: #fff; padding: 17px 32px; border-radius: 14px;
            font-size: 17px; font-weight: 600; font-family: 'Inter', sans-serif;
            border: none; cursor: pointer; margin-top: 20px;
            box-shadow: 0 4px 18px rgba(59,130,246,0.3);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }}
        .submit-button:hover {{ transform: translateY(-2px); box-shadow: 0 8px 28px rgba(59,130,246,0.4); }}
        #order-form-status {{ display: none; margin-top: 18px; padding: 14px; border-radius: 10px; font-weight: 800; text-align: center; }}
        .honeypot {{ position: absolute; left: -9999px; opacity: 0; pointer-events: none; }}

        /* Model Explorer */
        .model-explorer {{ background: #fff; border-radius: 16px; padding: 28px; box-shadow: 0 6px 24px rgba(0,0,0,0.06); border: 1px solid #eef1f4; }}
        .filter-bar {{ display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 20px; align-items: center; }}
        .filter-bar input[type="text"] {{
            flex: 1; min-width: 200px; padding: 10px 14px; border: 1px solid #e2e8f0; border-radius: 10px;
            font-size: 14px; background: #fafbfc; font-family: 'Inter', sans-serif;
        }}
        .filter-bar input[type="text"]:focus {{ outline: none; border-color: #3b82f6; background: #fff; }}
        .filter-bar select {{
            padding: 10px 14px; border: 1px solid #e2e8f0; border-radius: 10px;
            font-size: 14px; background: #fafbfc; font-family: 'Inter', sans-serif; cursor: pointer;
        }}
        .filter-bar select:focus {{ outline: none; border-color: #3b82f6; }}
        .filter-stats {{ font-size: 13px; color: #64748b; margin-bottom: 12px; }}
        .filter-stats strong {{ color: #3b82f6; }}
        .model-table-container {{ overflow-x: auto; max-height: 600px; overflow-y: auto; border-radius: 10px; border: 1px solid #e2e8f0; }}
        .model-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        .model-table thead {{ position: sticky; top: 0; z-index: 2; }}
        .model-table th {{ background: #1e293b; color: #e2e8f0; padding: 10px 14px; text-align: left; font-weight: 600; white-space: nowrap; cursor: pointer; user-select: none; }}
        .model-table th:hover {{ background: #334155; }}
        .model-table th .sort-icon {{ font-size: 10px; margin-left: 4px; opacity: 0.5; }}
        .model-table th.sorted .sort-icon {{ opacity: 1; }}
        .model-table td {{ padding: 8px 14px; border-bottom: 1px solid #f1f5f9; color: #374151; white-space: nowrap; }}
        .model-table tr:hover td {{ background: #f0f7ff; }}
        .model-table tr:nth-child(even) td {{ background: #fafbfc; }}
        .model-table tr:nth-child(even):hover td {{ background: #f0f7ff; }}
        .price-green {{ color: #059669; font-family: monospace; font-weight: 500; }}
        .tier-badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }}
        .tier-free {{ background: #d1fae5; color: #065f46; }}
        .tier-basic {{ background: #dbeafe; color: #1e40af; }}
        .tier-pro {{ background: #ede9fe; color: #5b21b6; }}
        .tier-premium {{ background: #fef3c7; color: #92400e; }}
        .provider-tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 500; background: #f1f5f9; color: #475569; }}
        .provider-openai {{ background: #d1fae5; color: #065f46; }}
        .provider-anthropic {{ background: #ede9fe; color: #5b21b6; }}
        .provider-google {{ background: #dbeafe; color: #1e40af; }}
        .provider-amazon {{ background: #fef3c7; color: #92400e; }}
        .provider-deepseek {{ background: #cffafe; color: #155e75; }}
        .provider-mistral {{ background: #ffedd5; color: #9a3412; }}
        .provider-deepinfra {{ background: #e0e7ff; color: #3730a3; }}
        .provider-xai {{ background: #fce7f3; color: #9d174d; }}
        .provider-cohere {{ background: #d1fae5; color: #065f46; }}
        .provider-minimax {{ background: #fef9c3; color: #854d0e; }}
        .provider-qwen {{ background: #e0f2fe; color: #075985; }}
        .provider-dashscope {{ background: #e0f2fe; color: #075985; }}
        .provider-databricks {{ background: #fee2e2; color: #991b1b; }}
        .provider-microsoft {{ background: #dbeafe; color: #1e40af; }}
        .provider-groq {{ background: #dcfce7; color: #166534; }}
        .provider-together_ai {{ background: #f3e8ff; color: #6b21a8; }}
        .provider-perplexityai {{ background: #e0e7ff; color: #4338ca; }}
        .provider-fireworks_ai {{ background: #ffedd5; color: #c2410c; }}
        .provider-bytedance {{ background: #cffafe; color: #0e7490; }}
        .provider-cerebras {{ background: #f0fdf4; color: #15803d; }}
        .provider-cloudflare {{ background: #fef3c7; color: #b45309; }}
        .provider-nebius {{ background: #e8d5ff; color: #7e22ce; }}
        .provider-ovhcloud {{ background: #f1f5f9; color: #334155; }}
        .provider-scaleway {{ background: #fce7f3; color: #be185d; }}
        .provider-lilac {{ background: #fdf4ff; color: #a21caf; }}

        @media (max-width: 768px) {{
            .hero-inner {{ grid-template-columns: 1fr; }}
            .plans-grid {{ grid-template-columns: 1fr; }}
            .form-section {{ padding: 28px 20px; }}
            .steps-grid {{ grid-template-columns: 1fr 1fr; }}
            .filter-bar {{ flex-direction: column; }}
        }}

        footer {{
            background: #1e293b; color: #f8f9fa; text-align: center; padding: 30px 0; margin-top: 60px;
        }}
        footer p {{ margin: 8px 0; }}
        .footer-contact {{ margin-top: 15px; }}
        .footer-contact a {{ color: #ffffff; text-decoration: none; transition: color 0.3s; margin: 0 15px; display: inline-flex; align-items: center; gap: 8px; }}
        .footer-contact a:hover {{ color: #60a5fa; }}
        .footer-contact svg {{ width: 20px; height: 20px; fill: currentColor; }}
        .footer-links {{ margin-top: 12px; font-size: 13px; }}
        .footer-links a {{ color: #94a3b8; text-decoration: none; margin: 0 10px; transition: color 0.3s; }}
        .footer-links a:hover {{ color: #ffffff; text-decoration: underline; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-inner">
                <div class="logo">
                    <a href="index.html"><img src="logo621.svg" alt="AWSDO.COM Logo" height="44"></a>
                </div>
                <nav>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="linux-server.html">Linux Cloud</a></li>
                        <li><a href="windows-server.html">Windows Servers</a></li>
                        <li><a href="performance-server.html">Performance</a></li>
                        <li><a href="api-tokens.html" class="active">AI API Tokens</a></li>
                    </ul>
                </nav>
            </div>
        </div>
    </header>

    <!-- Hero -->
    <section class="hero">
        <div class="container hero-inner">
            <div>
                <h1>AI API Tokens<br><span>Unified Access to 700+ Models</span></h1>
                <p>Access OpenAI, Anthropic, Google, DeepSeek, Mistral, xAI and more through a single API endpoint. Choose a plan, top up, and start building — official pricing with recharge bonuses that save you up to 50%.</p>
                <div class="hero-badges">
                    <span class="badge">🤖 {free_count + basic_count + pro_count + premium_count}+ Models</span>
                    <span class="badge">💰 Up to 50% Savings</span>
                    <span class="badge">🔑 Single API Key</span>
                    <span class="badge">⚡ Pay-As-You-Go</span>
                </div>
            </div>
            <div class="hero-visual">
                <div class="hero-stats">
                    <div class="hero-stat">
                        <div class="stat-value">{free_count}<span>+</span></div>
                        <div class="stat-label">Free Models</div>
                    </div>
                    <div class="hero-stat">
                        <div class="stat-value">{free_count + basic_count}<span>+</span></div>
                        <div class="stat-label">Basic Plan</div>
                    </div>
                    <div class="hero-stat">
                        <div class="stat-value">{free_count + basic_count + pro_count}<span>+</span></div>
                        <div class="stat-label">Pro Plan</div>
                    </div>
                    <div class="hero-stat">
                        <div class="stat-value">{free_count + basic_count + pro_count + premium_count}<span>+</span></div>
                        <div class="stat-label">Ultimate Plan</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <div class="container">
        <!-- Model Explorer -->
        <section class="section">
            <h2 class="section-title">Model Explorer</h2>
            <p class="section-subtitle">Browse, search and filter all {free_count + basic_count + pro_count + premium_count} models with official pricing. Click column headers to sort.</p>

            <div class="model-explorer">
                <div class="filter-bar">
                    <input type="text" id="modelSearch" placeholder="🔍 Search model name or provider...">
                    <select id="filterTier">
                        <option value="all">All Plans</option>
                        <option value="free">🆓 Always Free ({free_count})</option>
                        <option value="basic">⚡ Basic ({basic_count})</option>
                        <option value="pro">🚀 Pro ({pro_count})</option>
                        <option value="premium">👑 Ultimate ({premium_count})</option>
                    </select>
                    <select id="filterProvider">
                        <option value="all">All Providers</option>
                    </select>
                </div>
                <div class="filter-stats" id="filterStats">Showing <strong>{free_count + basic_count + pro_count + premium_count}</strong> of {free_count + basic_count + pro_count + premium_count} models</div>
                <div class="model-table-container">
                    <table class="model-table" id="modelTable">
                        <thead>
                            <tr>
                                <th data-sort="id">Model ID <span class="sort-icon">▼</span></th>
                                <th data-sort="provider">Provider <span class="sort-icon">▼</span></th>
                                <th data-sort="tier">Plan <span class="sort-icon">▼</span></th>
                                <th data-sort="input">Input $/M <span class="sort-icon">▼</span></th>
                                <th data-sort="output">Output $/M <span class="sort-icon">▼</span></th>
                                <th data-sort="ctx">Context <span class="sort-icon">▼</span></th>
                            </tr>
                        </thead>
                        <tbody id="modelTableBody"></tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- How it works -->
        <section class="section">
            <h2 class="section-title">How It Works</h2>
            <p class="section-subtitle">Get started with AI API tokens in four simple steps.</p>
            <div class="steps-grid">
                <div class="step-card"><div class="step-num">1</div><h4>Choose a Plan</h4><p>Pick the tier that fits your model needs and budget.</p></div>
                <div class="step-card"><div class="step-num">2</div><h4>Select Top-Up Amount</h4><p>Top up $100+ and get bonus credits depending on your plan.</p></div>
                <div class="step-card"><div class="step-num">3</div><h4>Submit Order</h4><p>Fill in your name &amp; email and submit your order.</p></div>
                <div class="step-card"><div class="step-num">4</div><h4>Start Building</h4><p>Receive your API key and start calling 700+ models instantly.</p></div>
            </div>
        </section>

        <!-- Combined: Choose Plan + Order Form -->
        <section class="section" style="padding-top:0;">
            <h2 class="section-title">Choose Your Plan &amp; Order</h2>
            <p class="section-subtitle">Every higher plan includes all models from lower plans. Models use official pricing — you save through our top-up bonuses.</p>

            <form id="order-form" class="form-section" style="max-width:1100px;">
                <input type="text" name="website" class="honeypot" tabindex="-1" autocomplete="off">

                <!-- Step 1: Select Plan -->
                <div class="form-step">
                    <h3><span class="step-icon">1</span> Select Your Plan</h3>
                    <div class="plans-grid">
                        <div class="plan-card plan-free selected" data-plan="free" onclick="selectPlan(this,'free')">
                            <input type="radio" name="selectedPlan" value="Always Free" checked>
                            <div class="plan-icon">🆓</div>
                            <h3>Always Free</h3>
                            <div class="plan-price">$0 Forever</div>
                            <div class="plan-desc">Free access to budget-friendly models. No credit card required.</div>
                            <div class="plan-range">Input ≤ $0.07/M tokens</div>
                            <div class="model-count">{free_count}</div>
                            <div class="model-count-label">models included</div>
                        </div>
                        <div class="plan-card plan-basic" data-plan="basic" onclick="selectPlan(this,'basic')">
                            <input type="radio" name="selectedPlan" value="Basic Plan">
                            <div class="plan-icon">⚡</div>
                            <h3>Basic Plan</h3>
                            <div class="plan-price">Top up $100 → get <strong>$150</strong></div>
                            <div class="plan-desc">Includes Free tier + mid-range models. Great for startups.</div>
                            <div class="plan-range">Input $0.07 ~ $1.00/M</div>
                            <div class="model-count">{free_count + basic_count}</div>
                            <div class="model-count-label">models included</div>
                        </div>
                        <div class="plan-card plan-pro" data-plan="pro" onclick="selectPlan(this,'pro')" style="padding-top:36px;">
                            <div class="plan-popular">⭐ MOST POPULAR</div>
                            <input type="radio" name="selectedPlan" value="Pro Plan">
                            <div class="plan-icon">🚀</div>
                            <h3>Pro Plan</h3>
                            <div class="plan-price">Top up $100 → get <strong>$180</strong></div>
                            <div class="plan-desc">Claude Sonnet, GPT-5, Gemini Pro. Best value for professionals.</div>
                            <div class="plan-range">Input $1.10 ~ $2.90/M</div>
                            <div class="model-count">{free_count + basic_count + pro_count}</div>
                            <div class="model-count-label">models included</div>
                        </div>
                        <div class="plan-card plan-premium" data-plan="premium" onclick="selectPlan(this,'premium')">
                            <input type="radio" name="selectedPlan" value="Ultimate Plan">
                            <div class="plan-icon">👑</div>
                            <h3>Ultimate Plan</h3>
                            <div class="plan-price">Top up $100 → get <strong>$200</strong></div>
                            <div class="plan-desc">All models unlocked. Effectively 50% off official pricing.</div>
                            <div class="plan-range">Input ≥ $3.00/M</div>
                            <div class="model-count">{free_count + basic_count + pro_count + premium_count}</div>
                            <div class="model-count-label">models included</div>
                        </div>
                    </div>
                </div>

                <!-- Step 2: Recharge (hidden for free) -->
                <div class="form-step" id="rechargeStep" style="display:none;">
                    <h3><span class="step-icon">2</span> Select Top-Up Amount</h3>
                    <p class="section-note">Choose how much to top up. Bonus credits are added automatically based on your plan.</p>
                    <div class="recharge-grid">
                        <div class="recharge-option selected" onclick="selectRecharge(this, 100)">
                            <input type="radio" name="rechargeAmount" value="100" checked>
                            <div class="amount">$100</div>
                            <div class="bonus" id="bonus100">+$50 bonus</div>
                            <div class="total" id="total100">= $150 total</div>
                        </div>
                        <div class="recharge-option" onclick="selectRecharge(this, 200)">
                            <input type="radio" name="rechargeAmount" value="200">
                            <div class="amount">$200</div>
                            <div class="bonus" id="bonus200">+$100 bonus</div>
                            <div class="total" id="total200">= $300 total</div>
                        </div>
                        <div class="recharge-option" onclick="selectRecharge(this, 500)">
                            <input type="radio" name="rechargeAmount" value="500">
                            <div class="amount">$500</div>
                            <div class="bonus" id="bonus500">+$250 bonus</div>
                            <div class="total" id="total500">= $750 total</div>
                        </div>
                        <div class="recharge-option" onclick="selectRecharge(this, 1000)">
                            <input type="radio" name="rechargeAmount" value="1000">
                            <div class="amount">$1000</div>
                            <div class="bonus" id="bonus1000">+$500 bonus</div>
                            <div class="total" id="total1000">= $1500 total</div>
                        </div>
                    </div>
                </div>

                <!-- Order Summary -->
                <div class="form-step">
                    <h3><span class="step-icon" id="summaryStepNum">2</span> Order Summary</h3>
                    <div class="order-summary">
                        <div class="row"><span class="label">Plan</span><span class="value" id="summaryPlan">Always Free</span></div>
                        <div class="row"><span class="label">Top-Up Amount</span><span class="value" id="summaryTopup">$0</span></div>
                        <div class="row"><span class="label">Bonus Credits</span><span class="value" id="summaryBonus" style="color:#16a34a;">$0</span></div>
                        <div class="row total"><span class="label">Total Available Credits</span><span class="value" id="summaryTotal">$0 (Free)</span></div>
                    </div>
                    <p class="section-note" id="planNote">🆓 The Always Free plan requires no payment. You get free access to {free_count} budget models.</p>
                </div>

                <!-- Contact Info -->
                <div class="form-step">
                    <h3><span class="step-icon" id="contactStepNum">3</span> Your Information</h3>
                    <div class="form-group">
                        <label for="userName">Your Name *</label>
                        <input type="text" id="userName" name="userName" required placeholder="Your full name">
                    </div>
                    <div class="form-group">
                        <label for="email">Your Email *</label>
                        <input type="email" id="email" name="email" required placeholder="you@example.com">
                    </div>
                </div>

                <button type="submit" class="submit-button">
                    <svg viewBox="0 0 24 24" fill="none" style="width:22px;height:22px;"><path d="M9 12l2 2 4-4" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="12" r="9" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"/></svg>
                    Submit Order
                    <svg viewBox="0 0 24 24" fill="none" style="width:22px;height:22px;"><path d="M5 12h14M13 6l6 6-6 6" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </button>
                <p id="order-form-status"></p>
            </form>
        </section>

    </div>

    <!-- Chatwoot -->
    <script>
      window.chatwootSettings = {{"position":"right","type":"expanded_bubble","launcherTitle":"Online Chat"}};
      (function(d,t) {{
        var BASE_URL="https://app.chatwoot.com/";
        var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
        g.src=BASE_URL+"/packs/js/sdk.js"; g.defer=true; g.async=true;
        s.parentNode.insertBefore(g,s);
        g.onload=function(){{ window.chatwootSDK.run({{ websiteToken:'c3stLVCV9GDjtvHcBMLdjRjU', baseUrl:BASE_URL }}) }}
      }})(document,"script");
    </script>

    <script>
    // All models data
    const ALL_MODELS = {models_json};

    const tierNames = {{ free:'Always Free', basic:'Basic', pro:'Pro', premium:'Ultimate' }};
    const tierOrder = {{ free:0, basic:1, pro:2, premium:3 }};

    // Populate provider filter
    const providers = [...new Set(ALL_MODELS.map(m => m.provider))].sort();
    const providerSelect = document.getElementById('filterProvider');
    providers.forEach(p => {{
        const opt = document.createElement('option');
        opt.value = p; opt.textContent = p;
        providerSelect.appendChild(opt);
    }});

    let currentSort = {{ key: 'input', asc: true }};
    let filteredModels = [...ALL_MODELS];

    function renderTable() {{
        const tbody = document.getElementById('modelTableBody');
        let html = '';
        filteredModels.forEach(m => {{
            html += '<tr>'
                + '<td>' + m.id + '</td>'
                + '<td><span class="provider-tag provider-' + m.provider + '">' + m.provider + '</span></td>'
                + '<td><span class="tier-badge tier-' + m.tier + '">' + tierNames[m.tier] + '</span></td>'
                + '<td class="price-green">$' + m.input + '</td>'
                + '<td class="price-green">$' + m.output + '</td>'
                + '<td>' + m.ctx + '</td>'
                + '</tr>';
        }});
        tbody.innerHTML = html;
        document.getElementById('filterStats').innerHTML = 'Showing <strong>' + filteredModels.length + '</strong> of ' + ALL_MODELS.length + ' models';
    }}

    function applyFilters() {{
        const q = document.getElementById('modelSearch').value.toLowerCase();
        const tier = document.getElementById('filterTier').value;
        const provider = document.getElementById('filterProvider').value;
        filteredModels = ALL_MODELS.filter(m => {{
            if (tier !== 'all' && m.tier !== tier) return false;
            if (provider !== 'all' && m.provider !== provider) return false;
            if (q && !(m.id.toLowerCase().includes(q) || m.provider.toLowerCase().includes(q))) return false;
            return true;
        }});
        applySort();
        renderTable();
    }}

    function applySort() {{
        const key = currentSort.key;
        const asc = currentSort.asc ? 1 : -1;
        filteredModels.sort((a, b) => {{
            let va = a[key], vb = b[key];
            if (key === 'input' || key === 'output') {{
                va = parseFloat(va) || 0;
                vb = parseFloat(vb) || 0;
            }} else if (key === 'tier') {{
                va = tierOrder[va] || 0;
                vb = tierOrder[vb] || 0;
            }} else {{
                va = String(va).toLowerCase();
                vb = String(vb).toLowerCase();
            }}
            if (va < vb) return -1 * asc;
            if (va > vb) return 1 * asc;
            return 0;
        }});
    }}

    // Sort on header click
    document.querySelectorAll('.model-table th[data-sort]').forEach(th => {{
        th.addEventListener('click', function() {{
            const key = this.dataset.sort;
            if (currentSort.key === key) {{ currentSort.asc = !currentSort.asc; }}
            else {{ currentSort.key = key; currentSort.asc = true; }}
            document.querySelectorAll('.model-table th').forEach(h => h.classList.remove('sorted'));
            this.classList.add('sorted');
            this.querySelector('.sort-icon').textContent = currentSort.asc ? '▲' : '▼';
            applySort();
            renderTable();
        }});
    }});

    document.getElementById('modelSearch').addEventListener('input', applyFilters);
    document.getElementById('filterTier').addEventListener('change', applyFilters);
    document.getElementById('filterProvider').addEventListener('change', applyFilters);

    // Initial render
    applyFilters();

    // ===== Plan & Order Logic =====
    const planConfig = {{
        free:    {{ name:'Always Free', bonusRate:0,   note:'🆓 The Always Free plan requires no payment. You get free access to {free_count} budget models.' }},
        basic:   {{ name:'Basic Plan',  bonusRate:0.5, note:'⚡ Top up $100 and get $50 bonus (33% savings). Access {free_count + basic_count}+ models.' }},
        pro:     {{ name:'Pro Plan',    bonusRate:0.8, note:'🚀 Top up $100 and get $80 bonus (44% savings). Access {free_count + basic_count + pro_count}+ models.' }},
        premium: {{ name:'Ultimate Plan',bonusRate:1.0,note:'👑 Top up $100 and get $100 bonus (50% savings). Access ALL {free_count + basic_count + pro_count + premium_count}+ models.' }}
    }};
    let currentPlan = 'free';
    let currentRecharge = 100;

    function selectPlan(card, plan) {{
        document.querySelectorAll('.plan-card').forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        card.querySelector('input[type="radio"]').checked = true;
        currentPlan = plan;
        const cfg = planConfig[plan];
        document.getElementById('planNote').innerHTML = cfg.note;
        if (plan === 'free') {{
            document.getElementById('rechargeStep').style.display = 'none';
            document.getElementById('summaryStepNum').textContent = '2';
            document.getElementById('contactStepNum').textContent = '3';
            updateSummary(0, 0);
        }} else {{
            document.getElementById('rechargeStep').style.display = 'block';
            document.getElementById('summaryStepNum').textContent = '3';
            document.getElementById('contactStepNum').textContent = '4';
            updateRechargeLabels();
            updateSummary(currentRecharge, currentRecharge * cfg.bonusRate);
        }}
    }}

    function selectRecharge(el, amount) {{
        document.querySelectorAll('.recharge-option').forEach(o => o.classList.remove('selected'));
        el.classList.add('selected');
        el.querySelector('input[type="radio"]').checked = true;
        currentRecharge = amount;
        updateSummary(amount, amount * planConfig[currentPlan].bonusRate);
    }}

    function updateRechargeLabels() {{
        const cfg = planConfig[currentPlan];
        [100,200,500,1000].forEach(amt => {{
            const bonus = amt * cfg.bonusRate;
            document.getElementById('bonus'+amt).textContent = '+$'+bonus+' bonus';
            document.getElementById('total'+amt).textContent = '= $'+(amt+bonus)+' total';
        }});
    }}

    function updateSummary(topup, bonus) {{
        const cfg = planConfig[currentPlan];
        document.getElementById('summaryPlan').textContent = cfg.name;
        if (currentPlan === 'free') {{
            document.getElementById('summaryTopup').textContent = '$0';
            document.getElementById('summaryBonus').textContent = '$0';
            document.getElementById('summaryTotal').textContent = '$0 (Free Tier)';
        }} else {{
            document.getElementById('summaryTopup').textContent = '$'+topup;
            document.getElementById('summaryBonus').textContent = '+$'+bonus;
            document.getElementById('summaryTotal').textContent = '$'+(topup+bonus);
        }}
    }}

    // Form submit
    const form = document.getElementById("order-form");
    const statusEl = document.getElementById("order-form-status");

    function showStatus(msg, tone) {{
        statusEl.style.display='block'; statusEl.textContent=msg;
        if(tone==='success'){{ statusEl.style.backgroundColor='#d1fae5'; statusEl.style.border='1px solid #6ee7b7'; statusEl.style.color='#065f46'; }}
        else if(tone==='error'){{ statusEl.style.backgroundColor='#fee2e2'; statusEl.style.border='1px solid #fca5a5'; statusEl.style.color='#991b1b'; }}
        else{{ statusEl.style.backgroundColor='#fef3c7'; statusEl.style.border='1px solid #fde68a'; statusEl.style.color='#92400e'; }}
    }}

    form.addEventListener("submit", function(event) {{
        event.preventDefault();
        const honeypot = document.querySelector('input[name="website"]');
        if (honeypot && honeypot.value) return false;
        const formData = new FormData(event.target);
        const userName = (formData.get('userName')||'').trim();
        const email = (formData.get('email')||'').trim();
        const plan = formData.get('selectedPlan') || 'Always Free';
        const rechargeAmount = currentPlan==='free' ? 0 : currentRecharge;
        const cfg = planConfig[currentPlan];
        const bonus = rechargeAmount * cfg.bonusRate;
        const totalCredits = rechargeAmount + bonus;

        if (!userName || !email) {{ showStatus('Please fill in both your name and email address.','error'); return; }}

        const overlay = document.createElement('div');
        overlay.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.55);z-index:9999;display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box;';
        overlay.innerHTML = `
            <div style="background:#fff;padding:32px 28px;border-radius:16px;max-width:520px;width:100%;text-align:center;box-shadow:0 20px 50px rgba(0,0,0,0.25);">
                <div style="font-size:2.6rem;margin-bottom:10px;">🤖</div>
                <h4 style="margin:0 0 14px;color:#333;">Confirm Your Order</h4>
                <div style="background:#f8f9fa;border-radius:10px;padding:16px;text-align:left;margin-bottom:18px;font-size:.93rem;line-height:1.9;">
                    <div><strong>Name:</strong> ${{userName}}</div>
                    <div><strong>Email:</strong> ${{email}}</div>
                    <div><strong>Plan:</strong> ${{plan}}</div>
                    <div><strong>Top-Up:</strong> $${{rechargeAmount}}</div>
                    <div><strong>Bonus:</strong> +$${{bonus}}</div>
                    <div><strong>Total Credits:</strong> <span style="color:#059669;font-weight:700;">$${{totalCredits}}</span></div>
                </div>
                <p style="font-size:.85rem;color:#888;margin-bottom:18px;">Our team will contact you to confirm payment and deliver your API key.</p>
                <button id="btn-confirm-ok" style="background:linear-gradient(135deg,#3b82f6,#6366f1);color:#fff;border:none;padding:12px 24px;border-radius:25px;font-weight:800;font-size:1rem;cursor:pointer;width:100%;margin-bottom:10px;">✅ Confirm &amp; Submit</button>
                <button id="btn-confirm-cancel" style="background:#f8f9fa;color:#666;border:1px solid #ddd;padding:10px 20px;border-radius:20px;cursor:pointer;font-size:.9rem;width:100%;">❌ Go Back</button>
            </div>`;
        document.body.appendChild(overlay);
        document.getElementById('btn-confirm-cancel').onclick = function(){{ document.body.removeChild(overlay); }};
        document.getElementById('btn-confirm-ok').onclick = function() {{
            document.body.removeChild(overlay);
            const comment = 'Name: '+userName+'\\nEmail: '+email+'\\nPlan: '+plan+'\\nTop-Up: $'+rechargeAmount+'\\nBonus: +$'+bonus+'\\nTotal Credits: $'+totalCredits;
            showStatus('Submitting your order…','info');
            fetch('https://api.notificationapi.com/097bululbdjfm969xrmrijiz43/sender', {{
                method:'POST',
                headers:{{ 'Content-Type':'application/json', 'Accept':'application/json',
                    'Authorization':'Basic MDk3YnVsdWxiZGpmbTk2OXhybXJpaml6NDM6c3c1MDFsdW1ib2w4ajNrYm1jMzJtdWd2aHNtdDBkd2NtaDQ3dDc3YXZ3enBvd3BiMTFjNXltdW1qeA==' }},
                body: JSON.stringify({{ type:'awsdo_com_notification', to:{{ id:'snaagk@gmail.com', email:'snaagk@gmail.com' }}, parameters:{{ comment:comment }}, templateId:'awsdo_com' }})
            }})
            .then(r => r.json().catch(()=>null))
            .then(() => {{ showStatus('✅ Order submitted successfully! We will contact you at '+email+' shortly with your API key.','success'); }})
            .catch(err => {{ console.error(err); showStatus('✅ Order received! We will contact you at '+email+' soon.','success'); }});
        }};
    }});
    </script>

    <footer>
        <div class="container">
            <p>&copy; 2026 AWSDO.COM. All rights reserved.</p>
            <div class="footer-contact">
                <a href="mailto:support@awsdo.com"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg> support@awsdo.com</a>
                <a href="https://t.me/ilovesunkeinfo" target="_blank"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 2L11 13H2l1.67-5.01L22 2zm-2.48 18.51L17 14l-4.2 4.13-1.67-5.01L2 13h9l2-2-8.5-8.5L22 2l-2.48 18.51z"/></svg> @ilovesunkeinfo</a>
            </div>
            <div class="footer-links">
                <a href="p/refund-policy.html">Refund Policy</a>
                <span style="color:#64748b;">|</span>
                <a href="p/terms-of-service.html">Terms of Service</a>
            </div>
        </div>
    </footer>
</body>
</html>'''

with open('api-tokens.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated api-tokens.html with {free_count + basic_count + pro_count + premium_count} total models")
print(f"  Free: {free_count}, Basic: {basic_count}, Pro: {pro_count}, Premium: {premium_count}")
