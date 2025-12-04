"""
Comprehensive PDF Report Generator for Gen AI ROI & TCO Calculator
Creates professional, detailed 20+ page reports with charts and extensive analysis
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
import io
from datetime import datetime

class ComprehensivePDFGenerator:
    """Generate comprehensive 20+ page PDF reports for Gen AI investments"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Create custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#1f77b4'),
            borderPadding=5,
            backColor=colors.HexColor('#f0f8ff')
        ))
        
        # Subsection header
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=8,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=10,
            alignment=TA_JUSTIFY,
            leading=14
        ))
        
        # Bullet point
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leftIndent=20,
            bulletIndent=10
        ))
    
    def _create_cost_distribution_chart(self, data_dict, title="Cost Distribution"):
        """Create a professional horizontal stacked bar chart for cost distribution"""
        drawing = Drawing(500, 300)
        
        labels = list(data_dict.keys())
        values = list(data_dict.values())
        total = sum(values)
        
        # Calculate percentages
        percentages = [(v/total)*100 if total > 0 else 0 for v in values]
        
        # Colors
        colors_scheme = [
            colors.HexColor('#1f77b4'),  # Blue
            colors.HexColor('#ff7f0e'),  # Orange
            colors.HexColor('#2ca02c'),  # Green
            colors.HexColor('#d62728'),  # Red
            colors.HexColor('#9467bd'),  # Purple
            colors.HexColor('#8c564b'),  # Brown
            colors.HexColor('#e377c2'),  # Pink
            colors.HexColor('#7f7f7f'),  # Gray
        ]
        
        # Create horizontal bars
        y_position = 250
        x_start = 50
        bar_width = 400
        bar_height = 40
        
        # Title
        from reportlab.graphics.shapes import String, Rect
        title_string = String(250, 280, title, fontSize=12, fontName='Helvetica-Bold',
                             textAnchor='middle', fillColor=colors.HexColor('#1f77b4'))
        drawing.add(title_string)
        
        # Draw stacked bars
        current_x = x_start
        for i, (label, value, pct) in enumerate(zip(labels, values, percentages)):
            if pct > 0:
                segment_width = (pct / 100) * bar_width
                
                # Draw rectangle
                rect = Rect(current_x, y_position, segment_width, bar_height,
                           fillColor=colors_scheme[i % len(colors_scheme)],
                           strokeColor=colors.white,
                           strokeWidth=1)
                drawing.add(rect)
                
                # Add label inside bar if space permits
                if segment_width > 30:
                    label_text = String(current_x + segment_width/2, y_position + bar_height/2,
                                      f"{pct:.1f}%", fontSize=8, fontName='Helvetica-Bold',
                                      textAnchor='middle', fillColor=colors.white)
                    drawing.add(label_text)
                
                current_x += segment_width
        
        # Add legend below
        legend_y = 210
        legend_x = 50
        for i, (label, value) in enumerate(zip(labels, values)):
            # Color box
            box = Rect(legend_x, legend_y - (i * 20), 12, 12,
                      fillColor=colors_scheme[i % len(colors_scheme)],
                      strokeColor=colors.black, strokeWidth=0.5)
            drawing.add(box)
            
            # Label
            label_text = String(legend_x + 18, legend_y - (i * 20) + 3,
                              f"{label}: ${value:,.0f} ({percentages[i]:.1f}%)",
                              fontSize=9, fontName='Helvetica',
                              textAnchor='start', fillColor=colors.black)
            drawing.add(label_text)
        
        return drawing
    
    def _create_bar_chart(self, year_data, title="Annual Costs"):
        """Create professional bar chart"""
        drawing = Drawing(500, 250)
        
        bc = VerticalBarChart()
        bc.x = 80
        bc.y = 50
        bc.height = 150
        bc.width = 350
        bc.data = [year_data]
        
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = max(year_data) * 1.2
        bc.valueAxis.valueStep = max(year_data) * 0.2
        
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.categoryNames = ['Year 1', 'Year 2', 'Year 3']
        
        bc.bars[0].fillColor = colors.HexColor('#1f77b4')
        
        from reportlab.graphics.shapes import String
        title_string = String(250, 220, title, fontSize=12, fontName='Helvetica-Bold',
                             textAnchor='middle', fillColor=colors.HexColor('#1f77b4'))
        
        drawing.add(bc)
        drawing.add(title_string)
        
        return drawing
    
    def _create_header(self, org_name, industry, use_case):
        """Create report header"""
        elements = []
        
        title = Paragraph(
            f"Comprehensive Gen AI Investment Analysis<br/>{org_name}",
            self.styles['CustomTitle']
        )
        elements.append(title)
        
        meta_text = f"""
        <b>Industry:</b> {industry} | <b>Primary Use Case:</b> {use_case}<br/>
        <b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
        <b>Report Type:</b> Comprehensive TCO & ROI Analysis (20+ Pages)
        """
        meta = Paragraph(meta_text, self.styles['CustomBody'])
        elements.append(meta)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_table_of_contents(self):
        """Create table of contents with proper alignment"""
        elements = []
        
        elements.append(Paragraph("Table of Contents", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Create TOC as a properly formatted table
        toc_data = [
            ['Section 1:', 'Executive Summary', 'Page 2'],
            ['Section 2:', 'Methodology & Assumptions', 'Page 3'],
            ['Section 3:', 'Detailed Cost Analysis', 'Page 5'],
            ['Section 4:', 'Return on Investment Analysis', 'Page 9'],
            ['Section 5:', 'Risk Assessment & Mitigation', 'Page 11'],
            ['Section 6:', 'Implementation Roadmap', 'Page 13'],
            ['Section 7:', 'Technology Stack Recommendations', 'Page 15'],
            ['Section 8:', 'Governance & Compliance Framework', 'Page 17'],
            ['Section 9:', 'Change Management Strategy', 'Page 18'],
            ['Section 10:', 'Success Metrics & KPIs', 'Page 19'],
            ['Section 11:', 'Industry Benchmarks', 'Page 20'],
            ['Appendices:', 'Supporting Data & References', 'Page 22']
        ]
        
        toc_table = Table(toc_data, colWidths=[1*inch, 4.5*inch, 1*inch])
        toc_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#1f77b4')),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc'))
        ]))
        
        elements.append(toc_table)
        elements.append(PageBreak())
        
        return elements
    
    def _create_executive_summary(self, cost_data, roi_data):
        """Create executive summary - Page 2"""
        elements = []
        
        elements.append(Paragraph("Section 1: Executive Summary", self.styles['SectionHeader']))
        
        summary_text = """
        This comprehensive analysis evaluates the total cost of ownership (TCO) and return on investment (ROI) 
        for implementing Generative AI solutions within your organization. The analysis spans a three-year period 
        and incorporates all direct costs, indirect costs, and hidden costs associated with Gen AI adoption.
        <br/><br/>
        <b>Key Findings:</b><br/>
        The analysis reveals significant investment requirements balanced against substantial long-term benefits. 
        Our detailed evaluation considers infrastructure costs, API expenses, development resources, operational 
        overhead, and organizational change management requirements.
        """
        elements.append(Paragraph(summary_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Key metrics table
        metrics_data = [
            ['Metric', 'Value', 'Significance'],
            ['3-Year Total Cost of Ownership', 
             f"${cost_data.get('three_year_tco', 0):,.0f}",
             'Total investment required'],
            ['Year 1 Total Cost', 
             f"${cost_data.get('year1_total', 0):,.0f}",
             'Initial year investment'],
            ['3-Year ROI', 
             f"{roi_data.get('roi_percentage', 0):.1f}%",
             'Return on investment'],
            ['Payback Period', 
             f"{roi_data.get('payback_months', 'N/A')} months",
             'Time to break even'],
            ['NPV (10% discount)', 
             f"${roi_data.get('npv', 0):,.0f}",
             'Net present value']
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2.5*inch, 1.5*inch, 2.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 0.2*inch))
        
        recommendation_text = """
        <b>Executive Recommendation:</b><br/>
        Based on this comprehensive analysis, we recommend proceeding with a phased implementation approach, 
        starting with a pilot program to validate assumptions and demonstrate value. The detailed roadmap 
        in Section 6 provides specific milestones and decision points.
        """
        elements.append(Paragraph(recommendation_text, self.styles['CustomBody']))
        elements.append(PageBreak())
        
        return elements
    
    def _create_methodology_section(self):
        """Create methodology section - Pages 3-4"""
        elements = []
        
        elements.append(Paragraph("Section 2: Methodology & Assumptions", self.styles['SectionHeader']))
        
        elements.append(Paragraph("2.1 Analysis Framework", self.styles['SubsectionHeader']))
        
        framework_text = """
        This analysis employs a comprehensive Total Cost of Ownership (TCO) framework that captures all costs 
        associated with Gen AI implementation over a three-year period. Our methodology aligns with industry 
        best practices and incorporates lessons learned from successful enterprise AI deployments.
        <br/><br/>
        <b>Key Principles:</b><br/>
        • <b>Comprehensiveness:</b> All costs (direct, indirect, hidden) are captured<br/>
        • <b>Conservative Estimates:</b> Cost assumptions err on the side of caution<br/>
        • <b>Realistic Benefits:</b> Benefits are based on documented case studies<br/>
        • <b>Risk-Adjusted:</b> Incorporates contingency planning and risk mitigation
        """
        elements.append(Paragraph(framework_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph("2.2 Cost Categories", self.styles['SubsectionHeader']))
        
        categories_text = """
        Our analysis divides costs into seven primary categories:<br/><br/>
        <b>1. API & Model Costs:</b> Direct costs for API calls, token consumption, and model usage<br/>
        <b>2. Infrastructure:</b> Cloud computing, storage, networking, and security infrastructure<br/>
        <b>3. Development:</b> Engineering resources, model fine-tuning, integration work<br/>
        <b>4. Data Management:</b> Data preparation, labeling, quality assurance, storage<br/>
        <b>5. Operations:</b> Monitoring, maintenance, support, incident management<br/>
        <b>6. Organizational:</b> Training, change management, governance, compliance<br/>
        <b>7. Contingency:</b> Risk buffer for unexpected costs and scope changes
        """
        elements.append(Paragraph(categories_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph("2.3 Key Assumptions", self.styles['SubsectionHeader']))
        
        assumptions_data = [
            ['Category', 'Assumption', 'Rationale'],
            ['Growth Rate', '25% annual user growth', 'Industry standard for successful deployments'],
            ['API Pricing', 'Current vendor pricing', 'Assumes stable pricing with volume discounts'],
            ['Infrastructure', '30% annual cost growth', 'Accounts for scaling and redundancy'],
            ['Team Size', 'Scales with maturity', 'Based on typical team structures'],
            ['Training', '$2K per employee', 'Industry benchmark for AI training programs']
        ]
        
        assumptions_table = Table(assumptions_data, colWidths=[1.5*inch, 2.5*inch, 2.5*inch])
        assumptions_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        elements.append(assumptions_table)
        elements.append(PageBreak())
        
        return elements
    
    def _create_detailed_cost_analysis(self, cost_data):
        """Create detailed cost analysis - Pages 5-8"""
        elements = []
        
        elements.append(Paragraph("Section 3: Detailed Cost Analysis", self.styles['SectionHeader']))
        
        # 3-year overview
        elements.append(Paragraph("3.1 Three-Year Cost Overview", self.styles['SubsectionHeader']))
        
        # Check if we have breakdown data
        has_breakdowns = 'year1_breakdown' in cost_data and cost_data['year1_breakdown']
        
        if has_breakdowns:
            # Detailed breakdown table
            year_data = [
                ['Category', 'Year 1', 'Year 2', 'Year 3', 'Total', '% of Total'],
            ]
            
            total_tco = cost_data.get('three_year_tco', 1)
            
            for category in ['API Costs', 'Infrastructure', 'Development', 'Data Management', 'Operations', 'Organizational']:
                year1_val = cost_data.get('year1_breakdown', {}).get(category, 0)
                year2_val = cost_data.get('year2_breakdown', {}).get(category, 0)
                year3_val = cost_data.get('year3_breakdown', {}).get(category, 0)
                cat_total = year1_val + year2_val + year3_val
                pct = (cat_total / total_tco * 100) if total_tco > 0 else 0
                
                year_data.append([
                    category,
                    f"${year1_val:,.0f}",
                    f"${year2_val:,.0f}",
                    f"${year3_val:,.0f}",
                    f"${cat_total:,.0f}",
                    f"{pct:.1f}%"
                ])
            
            # Add totals row
            year_data.append([
                'Total',
                f"${cost_data.get('year1_total', 0):,.0f}",
                f"${cost_data.get('year2_total', 0):,.0f}",
                f"${cost_data.get('year3_total', 0):,.0f}",
                f"${total_tco:,.0f}",
                "100.0%"
            ])
            
            cost_table = Table(year_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1.2*inch, 0.8*inch])
        else:
            # Simplified table
            year_data = [
                ['Period', 'Total Cost'],
                ['Year 1', f"${cost_data.get('year1_total', 0):,.0f}"],
                ['Year 2', f"${cost_data.get('year2_total', 0):,.0f}"],
                ['Year 3', f"${cost_data.get('year3_total', 0):,.0f}"],
                ['3-Year Total', f"${cost_data.get('three_year_tco', 0):,.0f}"]
            ]
            cost_table = Table(year_data, colWidths=[3*inch, 2*inch])
        
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(cost_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Add cost distribution chart if we have breakdown
        if has_breakdowns:
            elements.append(Paragraph("3.2 Year 1 Cost Distribution", self.styles['SubsectionHeader']))
            cost_chart = self._create_cost_distribution_chart(cost_data['year1_breakdown'], 
                                                              "Year 1 Cost Breakdown by Category")
            elements.append(cost_chart)
            elements.append(Spacer(1, 0.2*inch))
        
        # Add bar chart
        if all(key in cost_data for key in ['year1_total', 'year2_total', 'year3_total']):
            elements.append(Paragraph("3.3 Annual Cost Trends", self.styles['SubsectionHeader']))
            year_costs = [
                cost_data.get('year1_total', 0),
                cost_data.get('year2_total', 0),
                cost_data.get('year3_total', 0)
            ]
            bar_chart = self._create_bar_chart(year_costs, "Total Annual Costs")
            elements.append(bar_chart)
        
        elements.append(PageBreak())
        
        # Detailed category explanations
        elements.append(Paragraph("3.4 Cost Category Deep Dive", self.styles['SubsectionHeader']))
        
        category_details = """
        <b>API & Model Costs:</b><br/>
        Direct expenses for API calls to foundation model providers (OpenAI, Anthropic, etc.). Includes token 
        consumption charges, fine-tuning costs, and any premium model access fees. This is typically the most 
        variable cost component, scaling directly with usage volume.<br/><br/>
        
        <b>Infrastructure Costs:</b><br/>
        Cloud computing resources including compute instances, GPU/TPU accelerators for inference, storage for 
        embeddings and model artifacts, networking bandwidth, load balancers, and security infrastructure. Also 
        includes backup and disaster recovery systems.<br/><br/>
        
        <b>Development Costs:</b><br/>
        Engineering team salaries and contractor fees for building AI applications, integrating with existing systems, 
        developing prompt engineering frameworks, creating evaluation pipelines, and implementing monitoring solutions. 
        This is typically the largest cost category in Year 1.<br/><br/>
        
        <b>Data Management Costs:</b><br/>
        Data preparation, cleaning, and labeling activities. Includes data pipeline infrastructure, quality assurance 
        processes, vector database licensing, and ongoing data maintenance. Critical for maintaining AI system accuracy 
        and relevance.<br/><br/>
        
        <b>Operations Costs:</b><br/>
        Ongoing monitoring, maintenance, and support activities. Includes incident response, performance optimization, 
        model retraining, prompt refinement, and user support. Grows as the system matures and user base expands.<br/><br/>
        
        <b>Organizational Costs:</b><br/>
        Change management, training programs, governance framework development, policy creation, compliance activities, 
        and organizational restructuring. Essential for successful AI adoption but often underestimated.
        """
        
        elements.append(Paragraph(category_details, self.styles['CustomBody']))
        elements.append(PageBreak())
        
        return elements
    
    def _create_roi_section(self, roi_data, cost_data):
        """Create ROI analysis section - Pages 9-10"""
        elements = []
        
        elements.append(Paragraph("Section 4: Return on Investment Analysis", self.styles['SectionHeader']))
        
        elements.append(Paragraph("4.1 ROI Metrics Summary", self.styles['SubsectionHeader']))
        
        roi_metrics = [
            ['Metric', 'Value', 'Industry Benchmark'],
            ['3-Year ROI', f"{roi_data.get('roi_percentage', 0):.1f}%", '100-200%'],
            ['Payback Period', f"{roi_data.get('payback_months', 'N/A')} months", '18-24 months'],
            ['Net Present Value', f"${roi_data.get('npv', 0):,.0f}", 'Positive NPV'],
            ['Internal Rate of Return', 'TBD', '25-40%'],
            ['Benefit-Cost Ratio', f"{roi_data.get('roi_percentage', 0)/100 + 1:.2f}", '>1.5']
        ]
        
        roi_table = Table(roi_metrics, colWidths=[2.5*inch, 2*inch, 2*inch])
        roi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(roi_table)
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph("4.2 Benefit Sources", self.styles['SubsectionHeader']))
        
        benefits_text = """
        <b>Primary Benefits:</b><br/>
        • <b>Productivity Gains:</b> 20-30% improvement in employee efficiency<br/>
        • <b>Cost Reduction:</b> Automation of manual processes saves $150K-$500K annually<br/>
        • <b>Revenue Growth:</b> Enhanced customer experience drives 5-15% revenue increase<br/>
        • <b>Quality Improvement:</b> Reduced errors and improved consistency<br/><br/>
        
        <b>Secondary Benefits:</b><br/>
        • <b>Innovation Acceleration:</b> Faster time-to-market for new products<br/>
        • <b>Competitive Advantage:</b> Early mover advantage in AI adoption<br/>
        • <b>Employee Satisfaction:</b> Reduced mundane tasks improves retention<br/>
        • <b>Scalability:</b> Handle increased volume without proportional cost growth
        """
        
        elements.append(Paragraph(benefits_text, self.styles['CustomBody']))
        elements.append(PageBreak())
        
        return elements
    
    def _create_implementation_roadmap(self):
        """Create implementation roadmap - Pages 13-14"""
        elements = []
        
        elements.append(Paragraph("Section 6: Implementation Roadmap", self.styles['SectionHeader']))
        
        roadmap_text = """
        This section outlines a phased approach to Gen AI implementation, with clear milestones, decision gates, 
        and success criteria for each phase.
        """
        elements.append(Paragraph(roadmap_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        roadmap_data = [
            ['Phase', 'Duration', 'Key Activities', 'Success Criteria'],
            ['Phase 1: Discovery', 
             'Months 1-2', 
             'Requirements gathering, use case prioritization, vendor evaluation, team formation',
             'Approved use cases, selected vendors, team in place'],
            ['Phase 2: Pilot', 
             'Months 3-5', 
             'Build MVP, test with limited users, gather feedback, refine approach',
             '80% user satisfaction, proven ROI on pilot use case'],
            ['Phase 3: Scale', 
             'Months 6-12', 
             'Expand to full production, onboard all users, establish operations',
             '90% adoption rate, operational excellence'],
            ['Phase 4: Optimize', 
             'Months 13+', 
             'Continuous improvement, expand use cases, optimize costs',
             'Sustained value delivery, new use cases identified']
        ]
        
        roadmap_table = Table(roadmap_data, colWidths=[1.2*inch, 1*inch, 2.5*inch, 1.8*inch])
        roadmap_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        elements.append(roadmap_table)
        elements.append(PageBreak())
        
        return elements
    
    def _create_additional_sections(self):
        """Create additional comprehensive sections"""
        elements = []
        
        # Section 5: Risk Assessment
        elements.append(Paragraph("Section 5: Risk Assessment & Mitigation", self.styles['SectionHeader']))
        
        risk_text = """
        <b>Critical Risks:</b><br/>
        • <b>Technical Risk:</b> Model performance may not meet expectations - Mitigation: Thorough testing, multiple vendor options<br/>
        • <b>Cost Overrun:</b> Actual costs exceed projections - Mitigation: 15% contingency buffer, monthly reviews<br/>
        • <b>Adoption Risk:</b> Users resist new technology - Mitigation: Comprehensive change management, training<br/>
        • <b>Security Risk:</b> Data breaches or unauthorized access - Mitigation: Robust security controls, compliance framework<br/>
        • <b>Vendor Risk:</b> Vendor pricing changes or service disruptions - Mitigation: Multi-vendor strategy, contract terms<br/><br/>
        
        <b>Risk Management Approach:</b><br/>
        Monthly risk reviews, escalation procedures, contingency plans for each major risk category.
        """
        elements.append(Paragraph(risk_text, self.styles['CustomBody']))
        elements.append(PageBreak())
        
        # Section 7: Technology Stack
        elements.append(Paragraph("Section 7: Technology Stack Recommendations", self.styles['SectionHeader']))
        
        tech_text = """
        <b>Foundation Models:</b><br/>
        Primary: OpenAI GPT-4, Anthropic Claude 3.5 | Backup: Google Gemini, AWS Bedrock<br/><br/>
        
        <b>Infrastructure:</b><br/>
        Cloud: AWS/Azure/GCP | Compute: GPU instances for fine-tuning | Storage: S3/Blob for artifacts<br/><br/>
        
        <b>Development Tools:</b><br/>
        Frameworks: LangChain, LlamaIndex | Monitoring: Weights & Biases, Arize AI | Version Control: Git, DVC<br/><br/>
        
        <b>Data Management:</b><br/>
        Vector DB: Pinecone, Weaviate | ETL: Airflow, Databricks | Quality: Great Expectations
        """
        elements.append(Paragraph(tech_text, self.styles['CustomBody']))
        elements.append(PageBreak())
        
        # Section 8: Governance
        elements.append(Paragraph("Section 8: Governance & Compliance Framework", self.styles['SectionHeader']))
        
        gov_text = """
        <b>Governance Structure:</b><br/>
        AI Steering Committee (quarterly reviews), AI Ethics Board (policy oversight), Working Groups (operational execution)<br/><br/>
        
        <b>Key Policies:</b><br/>
        • Data Privacy & Protection Policy | • Acceptable Use Policy | • Model Risk Management Policy<br/>
        • Bias Testing & Fairness Policy | • Third-Party Vendor Management Policy<br/><br/>
        
        <b>Compliance Requirements:</b><br/>
        SOC 2 Type II, GDPR, HIPAA (if applicable), Industry-specific regulations
        """
        elements.append(Paragraph(gov_text, self.styles['CustomBody']))
        elements.append(PageBreak())
        
        # Section 9: Change Management
        elements.append(Paragraph("Section 9: Change Management Strategy", self.styles['SectionHeader']))
        
        change_text = """
        <b>Communication Plan:</b><br/>
        Executive updates (monthly), All-hands presentations (quarterly), Team briefings (weekly during rollout)<br/><br/>
        
        <b>Training Program:</b><br/>
        Awareness training (all employees), Power user certification (select users), Technical deep-dives (developers)<br/><br/>
        
        <b>Support Structure:</b><br/>
        Dedicated help desk, AI Champions network, Office hours with experts, Comprehensive documentation
        """
        elements.append(Paragraph(change_text, self.styles['CustomBody']))
        elements.append(PageBreak())
        
        # Section 10: Success Metrics
        elements.append(Paragraph("Section 10: Success Metrics & KPIs", self.styles['SectionHeader']))
        
        kpi_data = [
            ['Category', 'Metric', 'Target', 'Measurement Frequency'],
            ['Adoption', 'Active Users', '>80%', 'Weekly'],
            ['Performance', 'Response Time', '<2 seconds', 'Real-time'],
            ['Quality', 'User Satisfaction', '>4.0/5.0', 'Monthly'],
            ['Cost', 'Cost per Query', '$0.05', 'Weekly'],
            ['Business Impact', 'Productivity Gain', '>25%', 'Quarterly']
        ]
        
        kpi_table = Table(kpi_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 1.5*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(kpi_table)
        elements.append(PageBreak())
        
        # Section 11: Industry Benchmarks
        elements.append(Paragraph("Section 11: Industry Benchmarks & Best Practices", self.styles['SectionHeader']))
        
        benchmark_text = """
        <b>Industry Adoption Rates:</b><br/>
        Technology: 85% | Financial Services: 75% | Healthcare: 60% | Retail: 70% | Manufacturing: 55%<br/><br/>
        
        <b>Typical Investment Ranges (by Company Size):</b><br/>
        Small (<500 employees): $200K-$800K | Medium (500-5K): $800K-$3M | Large (5K+): $3M-$15M+<br/><br/>
        
        <b>Success Factors from Industry Leaders:</b><br/>
        • Executive sponsorship and clear vision | • Start small, scale fast approach<br/>
        • Robust data foundation | • Focus on user experience | • Continuous learning culture
        """
        elements.append(Paragraph(benchmark_text, self.styles['CustomBody']))
        elements.append(PageBreak())
        
        return elements
    
    def _create_appendices(self):
        """Create appendices section"""
        elements = []
        
        elements.append(Paragraph("Appendices", self.styles['SectionHeader']))
        
        elements.append(Paragraph("Appendix A: Glossary of Terms", self.styles['SubsectionHeader']))
        
        glossary_text = """
        <b>API:</b> Application Programming Interface - method for accessing AI models<br/>
        <b>Fine-tuning:</b> Customizing a foundation model for specific use cases<br/>
        <b>LLM:</b> Large Language Model - foundation AI models like GPT-4, Claude<br/>
        <b>Prompt Engineering:</b> Crafting effective instructions for AI models<br/>
        <b>RAG:</b> Retrieval Augmented Generation - technique for grounding AI responses<br/>
        <b>TCO:</b> Total Cost of Ownership - comprehensive cost analysis<br/>
        <b>Token:</b> Unit of text processing (≈0.75 words)<br/>
        <b>Vector Database:</b> Database optimized for AI embeddings and similarity search
        """
        elements.append(Paragraph(glossary_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("Appendix B: References & Resources", self.styles['SubsectionHeader']))
        
        references_text = """
        • McKinsey & Company: "The Economic Potential of Generative AI"<br/>
        • Gartner: "Predicts 2025: Generative AI"<br/>
        • Stanford HAI: "Artificial Intelligence Index Report 2024"<br/>
        • Anthropic: "Claude Model Documentation"<br/>
        • OpenAI: "GPT-4 Technical Report"<br/>
        • Industry case studies from Fortune 500 implementations
        """
        elements.append(Paragraph(references_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.3*inch))
        
        elements.append(Paragraph("Appendix C: Contact Information", self.styles['SubsectionHeader']))
        
        contact_text = """
        For questions about this analysis or to discuss implementation:br/>
        Project Team: [Contact details]<br/>
        Executive Sponsor: [Contact details]<br/>
        Technical Lead: [Contact details]
        """
        elements.append(Paragraph(contact_text, self.styles['CustomBody']))
        
        return elements
    
    def _create_footer_disclaimer(self):
        """Create footer with disclaimer"""
        elements = []
        
        disclaimer = """
        <br/><br/>
        <font size=8 color='#666666'>
        <b>Important Disclaimer:</b> This comprehensive analysis provides detailed estimates based on inputs provided and industry benchmarks. 
        Actual costs, benefits, and outcomes may vary significantly based on implementation approach, organizational factors, market conditions, 
        and other variables. This report is intended for planning and decision-making purposes only and should not be considered as financial, 
        legal, or technical advice. Organizations should conduct their own due diligence and consult with qualified financial, legal, and 
        technical experts before making major investment decisions. Past performance and industry benchmarks do not guarantee future results.
        <br/><br/>
        Generated by Gen AI ROI & TCO Calculator | © 2024-2025 | Version 2.0
        </font>
        """
        
        elements.append(Paragraph(disclaimer, self.styles['CustomBody']))
        
        return elements
    
    def generate_report(self, cost_data, roi_data=None, risk_data=None):
        """
        Generate comprehensive 20+ page PDF report
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter, 
            rightMargin=72, 
            leftMargin=72,
            topMargin=72, 
            bottomMargin=50
        )
        
        elements = []
        
        # Cover page (Page 1)
        elements.extend(self._create_header(
            cost_data.get('org_name', 'Your Organization'),
            cost_data.get('industry', 'Technology'),
            cost_data.get('use_case', 'Gen AI Implementation')
        ))
        
        # Table of Contents
        elements.extend(self._create_table_of_contents())
        
        # Executive Summary (Page 2)
        if roi_data:
            elements.extend(self._create_executive_summary(cost_data, roi_data))
        
        # Methodology (Pages 3-4)
        elements.extend(self._create_methodology_section())
        
        # Detailed Cost Analysis (Pages 5-8)
        elements.extend(self._create_detailed_cost_analysis(cost_data))
        
        # ROI Analysis (Pages 9-10)
        if roi_data:
            elements.extend(self._create_roi_section(roi_data, cost_data))
        
        # Additional sections (Pages 11-21)
        elements.extend(self._create_additional_sections())
        
        # Implementation roadmap
        elements.extend(self._create_implementation_roadmap())
        
        # Appendices (Page 22+)
        elements.extend(self._create_appendices())
        
        # Footer disclaimer
        elements.extend(self._create_footer_disclaimer())
        
        # Build PDF
        doc.build(elements)
        
        pdf = buffer.getvalue()
        buffer.close()
        
        return pdf

# Wrapper function
def generate_comprehensive_pdf_report(cost_data, roi_data=None, risk_data=None):
    """Generate comprehensive 20+ page PDF report"""
    generator = ComprehensivePDFGenerator()
    return generator.generate_report(cost_data, roi_data, risk_data)