"""
PDF Report Generator for Gen AI ROI & TCO Calculator
Creates professional, comprehensive PDF reports with charts and analysis
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
import io
from datetime import datetime

class PDFReportGenerator:
    """Generate comprehensive PDF reports for Gen AI investments"""
    
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
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=12,
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
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=10,
            alignment=TA_JUSTIFY
        ))
        
        # Metric style
        self.styles.add(ParagraphStyle(
            name='MetricValue',
            parent=self.styles['Normal'],
            fontSize=18,
            textColor=colors.HexColor('#1f77b4'),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        ))
    
    def _create_header(self, org_name, industry, use_case):
        """Create report header"""
        elements = []
        
        # Title
        title = Paragraph(
            f"Gen AI Investment Analysis<br/>{org_name}",
            self.styles['CustomTitle']
        )
        elements.append(title)
        
        # Metadata
        meta_text = f"""
        <b>Industry:</b> {industry} | <b>Use Case:</b> {use_case}<br/>
        <b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        """
        meta = Paragraph(meta_text, self.styles['CustomBody'])
        elements.append(meta)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_executive_summary(self, cost_data, roi_data):
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        # Key metrics table
        metrics_data = [
            ['Metric', 'Value'],
            ['3-Year Total Cost of Ownership', f"${cost_data['three_year_tco']:,.0f}"],
            ['Year 1 Total Cost', f"${cost_data['year1_total']:,.0f}"],
            ['3-Year ROI', f"{roi_data.get('roi_percentage', 0):.1f}%"],
            ['Payback Period', f"{roi_data.get('payback_months', 'N/A')} months"],
            ['NPV (10% discount)', f"${roi_data.get('npv', 0):,.0f}"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_pie_chart(self, data_dict, title="Cost Distribution"):
        """Create a beautiful pie chart"""
        drawing = Drawing(400, 200)
        
        # Prepare data
        labels = list(data_dict.keys())
        values = list(data_dict.values())
        
        # Create pie chart
        pie = Pie()
        pie.x = 80
        pie.y = 20
        pie.width = 150
        pie.height = 150
        pie.data = values
        pie.labels = [f'{label}\n${value:,.0f}' for label, value in zip(labels, values)]
        pie.slices.strokeWidth = 0.5
        
        # Beautiful color scheme
        colors_scheme = [
            colors.HexColor('#1f77b4'),  # Blue
            colors.HexColor('#ff7f0e'),  # Orange
            colors.HexColor('#2ca02c'),  # Green
            colors.HexColor('#d62728'),  # Red
            colors.HexColor('#9467bd'),  # Purple
            colors.HexColor('#8c564b'),  # Brown
            colors.HexColor('#e377c2'),  # Pink
        ]
        
        for i, color in enumerate(colors_scheme[:len(values)]):
            pie.slices[i].fillColor = color
        
        # Add title
        from reportlab.graphics.shapes import String
        title_string = String(200, 180, title, fontSize=12, fontName='Helvetica-Bold', 
                             textAnchor='middle', fillColor=colors.HexColor('#1f77b4'))
        
        drawing.add(pie)
        drawing.add(title_string)
        
        return drawing
    
    def _create_bar_chart(self, year_data, title="Annual Costs"):
        """Create a beautiful bar chart for year-over-year costs"""
        drawing = Drawing(400, 200)
        
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 300
        bc.data = [year_data]
        
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = max(year_data) * 1.2
        bc.valueAxis.valueStep = max(year_data) * 0.2
        
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.categoryNames = ['Year 1', 'Year 2', 'Year 3']
        
        # Beautiful blue gradient colors
        bc.bars[0].fillColor = colors.HexColor('#1f77b4')
        
        # Add title
        from reportlab.graphics.shapes import String
        title_string = String(200, 180, title, fontSize=12, fontName='Helvetica-Bold',
                             textAnchor='middle', fillColor=colors.HexColor('#1f77b4'))
        
        drawing.add(bc)
        drawing.add(title_string)
        
        return drawing
    
    def _create_roi_chart(self, cost_data, roi_data):
        """Create cumulative cost vs benefit chart"""
        drawing = Drawing(400, 200)
        
        lc = HorizontalLineChart()
        lc.x = 50
        lc.y = 50
        lc.height = 125
        lc.width = 300
        
        # Cumulative costs and benefits
        year1_cost = cost_data['year1_total']
        year2_cost = cost_data['year1_total'] + cost_data['year2_total']
        year3_cost = cost_data['three_year_tco']
        
        # Estimate benefits progression
        total_benefits = roi_data.get('total_benefits', year3_cost * 2)
        year1_benefit = total_benefits * 0.2
        year2_benefit = total_benefits * 0.5
        year3_benefit = total_benefits
        
        lc.data = [
            [year1_cost, year2_cost, year3_cost],  # Costs
            [year1_benefit, year2_benefit, year3_benefit]  # Benefits
        ]
        
        lc.lines[0].strokeColor = colors.HexColor('#d62728')  # Red for costs
        lc.lines[1].strokeColor = colors.HexColor('#2ca02c')  # Green for benefits
        lc.lines[0].strokeWidth = 2
        lc.lines[1].strokeWidth = 2
        
        lc.valueAxis.valueMin = 0
        lc.valueAxis.valueMax = max(year3_cost, year3_benefit) * 1.1
        
        lc.categoryAxis.categoryNames = ['Year 1', 'Year 2', 'Year 3']
        lc.categoryAxis.labels.boxAnchor = 'n'
        
        # Add title and legend
        from reportlab.graphics.shapes import String, Rect
        title_string = String(200, 180, "Cumulative Costs vs Benefits", fontSize=12, 
                             fontName='Helvetica-Bold', textAnchor='middle',
                             fillColor=colors.HexColor('#1f77b4'))
        
        # Legend
        legend_cost = Rect(260, 165, 10, 10, fillColor=colors.HexColor('#d62728'))
        legend_benefit = Rect(260, 150, 10, 10, fillColor=colors.HexColor('#2ca02c'))
        legend_cost_text = String(275, 168, "Costs", fontSize=9)
        legend_benefit_text = String(275, 153, "Benefits", fontSize=9)
        
        drawing.add(lc)
        drawing.add(title_string)
        drawing.add(legend_cost)
        drawing.add(legend_benefit)
        drawing.add(legend_cost_text)
        drawing.add(legend_benefit_text)
        
        return drawing
    
    def _create_cost_breakdown(self, cost_data):
        """Create detailed cost breakdown section"""
        elements = []
        
        elements.append(Paragraph("3-Year Cost Breakdown", self.styles['SectionHeader']))
        
        # Year-by-year costs
        year_data = [
            ['Category', 'Year 1', 'Year 2', 'Year 3', 'Total'],
            ['API Costs', 
             f"${cost_data['year1_breakdown']['API Costs']:,.0f}",
             f"${cost_data['year2_breakdown']['API Costs']:,.0f}",
             f"${cost_data['year3_breakdown']['API Costs']:,.0f}",
             f"${sum([cost_data[f'year{i}_breakdown']['API Costs'] for i in range(1,4)]):,.0f}"],
            ['Infrastructure',
             f"${cost_data['year1_breakdown']['Infrastructure']:,.0f}",
             f"${cost_data['year2_breakdown']['Infrastructure']:,.0f}",
             f"${cost_data['year3_breakdown']['Infrastructure']:,.0f}",
             f"${sum([cost_data[f'year{i}_breakdown']['Infrastructure'] for i in range(1,4)]):,.0f}"],
            ['Development',
             f"${cost_data['year1_breakdown']['Development']:,.0f}",
             f"${cost_data['year2_breakdown']['Development']:,.0f}",
             f"${cost_data['year3_breakdown']['Development']:,.0f}",
             f"${sum([cost_data[f'year{i}_breakdown']['Development'] for i in range(1,4)]):,.0f}"],
            ['Data Management',
             f"${cost_data['year1_breakdown']['Data Management']:,.0f}",
             f"${cost_data['year2_breakdown']['Data Management']:,.0f}",
             f"${cost_data['year3_breakdown']['Data Management']:,.0f}",
             f"${sum([cost_data[f'year{i}_breakdown']['Data Management'] for i in range(1,4)]):,.0f}"],
            ['Operations',
             f"${cost_data['year1_breakdown']['Operations']:,.0f}",
             f"${cost_data['year2_breakdown']['Operations']:,.0f}",
             f"${cost_data['year3_breakdown']['Operations']:,.0f}",
             f"${sum([cost_data[f'year{i}_breakdown']['Operations'] for i in range(1,4)]):,.0f}"],
            ['Organizational',
             f"${cost_data['year1_breakdown']['Organizational']:,.0f}",
             f"${cost_data['year2_breakdown']['Organizational']:,.0f}",
             f"${cost_data['year3_breakdown']['Organizational']:,.0f}",
             f"${sum([cost_data[f'year{i}_breakdown']['Organizational'] for i in range(1,4)]):,.0f}"],
            ['Total',
             f"${cost_data['year1_total']:,.0f}",
             f"${cost_data['year2_total']:,.0f}",
             f"${cost_data['year3_total']:,.0f}",
             f"${cost_data['three_year_tco']:,.0f}"]
        ]
        
        cost_table = Table(year_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (0, -2), colors.lightgrey),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9)
        ]))
        
        elements.append(cost_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add Year 1 Cost Distribution Pie Chart
        elements.append(Paragraph("Year 1 Cost Distribution", self.styles['CustomSubtitle']))
        pie_chart = self._create_pie_chart(cost_data['year1_breakdown'], "Year 1 Costs by Category")
        elements.append(pie_chart)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add Year-over-Year Bar Chart
        elements.append(Paragraph("Annual Cost Trend", self.styles['CustomSubtitle']))
        year_costs = [cost_data['year1_total'], cost_data['year2_total'], cost_data['year3_total']]
        bar_chart = self._create_bar_chart(year_costs, "Total Costs by Year")
        elements.append(bar_chart)
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_roi_analysis(self, roi_data, cost_data=None):
        """Create ROI analysis section"""
        elements = []
        
        elements.append(Paragraph("Return on Investment Analysis", self.styles['SectionHeader']))
        
        # ROI metrics
        roi_metrics = [
            ['Metric', 'Value'],
            ['Total Benefits (3 years)', f"${roi_data.get('total_benefits', 0):,.0f}"],
            ['Total Costs (3 years)', f"${roi_data.get('total_costs', 0):,.0f}"],
            ['Net Benefit', f"${roi_data.get('net_benefit', 0):,.0f}"],
            ['ROI Percentage', f"{roi_data.get('roi_percentage', 0):.1f}%"],
            ['Payback Period', f"{roi_data.get('payback_months', 'N/A')} months"],
            ['Break-even Month', f"Month {roi_data.get('payback_months', 'N/A')}"],
            ['NPV (10% discount rate)', f"${roi_data.get('npv', 0):,.0f}"]
        ]
        
        roi_table = Table(roi_metrics, colWidths=[3*inch, 2*inch])
        roi_table.setStyle(TableStyle([
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
        
        elements.append(roi_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add Cumulative Costs vs Benefits Chart
        if cost_data:
            elements.append(Paragraph("Investment Payback Visualization", self.styles['CustomSubtitle']))
            roi_chart = self._create_roi_chart(cost_data, roi_data)
            elements.append(roi_chart)
            elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_risk_summary(self, risk_data):
        """Create risk assessment summary"""
        elements = []
        
        if not risk_data:
            return elements
        
        elements.append(Paragraph("Risk Assessment Summary", self.styles['SectionHeader']))
        
        risk_text = f"""
        <b>Overall Risk Level:</b> {risk_data.get('overall_risk', 'Not assessed')}<br/>
        <b>Key Risk Areas Identified:</b> {risk_data.get('risk_count', 0)} risks flagged<br/>
        <br/>
        <b>Recommendations:</b><br/>
        • Implement comprehensive risk mitigation strategies<br/>
        • Regular monitoring and review of risk factors<br/>
        • Establish contingency plans for high-risk areas<br/>
        • Ensure adequate resources for risk management
        """
        
        elements.append(Paragraph(risk_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_recommendations(self):
        """Create recommendations section"""
        elements = []
        
        elements.append(Paragraph("Strategic Recommendations", self.styles['SectionHeader']))
        
        recommendations = """
        <b>1. Cost Optimization:</b><br/>
        • Implement API request batching to reduce costs by 15-20%<br/>
        • Consider open-source models for non-critical workloads<br/>
        • Right-size infrastructure based on actual usage patterns<br/>
        <br/>
        <b>2. Implementation Strategy:</b><br/>
        • Start with pilot program to validate assumptions<br/>
        • Establish clear success metrics and KPIs<br/>
        • Plan for iterative scaling based on results<br/>
        <br/>
        <b>3. Risk Mitigation:</b><br/>
        • Develop comprehensive data governance framework<br/>
        • Implement robust security and compliance controls<br/>
        • Create contingency plans for key risk areas<br/>
        <br/>
        <b>4. Success Factors:</b><br/>
        • Executive sponsorship and organizational buy-in<br/>
        • Adequate training and change management<br/>
        • Regular monitoring and adjustment of approach
        """
        
        elements.append(Paragraph(recommendations, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.2*inch))
        
        return elements
    
    def _create_footer_disclaimer(self):
        """Create footer with disclaimer"""
        elements = []
        
        disclaimer = """
        <br/><br/>
        <font size=8 color='#666666'>
        <b>Disclaimer:</b> This calculator provides estimates based on inputs provided. 
        Actual costs and benefits may vary. Consult with financial and technical experts 
        for major investment decisions. This report is for planning purposes only and 
        should not be considered as financial advice.
        </font>
        """
        
        elements.append(Paragraph(disclaimer, self.styles['CustomBody']))
        
        return elements
    
    def generate_report(self, cost_data, roi_data=None, risk_data=None):
        """
        Generate complete PDF report
        
        Args:
            cost_data: Dictionary containing cost analysis data
            roi_data: Dictionary containing ROI calculation data
            risk_data: Dictionary containing risk assessment data
            
        Returns:
            BytesIO object containing the PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Header
        elements.extend(self._create_header(
            cost_data.get('org_name', 'Your Organization'),
            cost_data.get('industry', 'N/A'),
            cost_data.get('use_case', 'N/A')
        ))
        
        # Executive Summary
        if roi_data:
            elements.extend(self._create_executive_summary(cost_data, roi_data))
        
        # Cost Breakdown
        elements.extend(self._create_cost_breakdown(cost_data))
        
        # Page break before ROI section
        elements.append(PageBreak())
        
        # ROI Analysis
        if roi_data:
            elements.extend(self._create_roi_analysis(roi_data, cost_data))
        
        # Risk Summary
        if risk_data:
            elements.extend(self._create_risk_summary(risk_data))
        
        # Recommendations
        elements.extend(self._create_recommendations())
        
        # Footer disclaimer
        elements.extend(self._create_footer_disclaimer())
        
        # Build PDF
        doc.build(elements)
        
        # Get the value of the BytesIO buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        return pdf

# Convenience function for Streamlit integration
def generate_pdf_report(cost_data, roi_data=None, risk_data=None):
    """
    Generate PDF report - wrapper function for Streamlit
    
    Returns:
        bytes: PDF file content
    """
    generator = PDFReportGenerator()
    return generator.generate_report(cost_data, roi_data, risk_data)