"""telecom-spec-dependency-slide-generator package."""

from .dependency_analyzer import DependencyAnalyzer
from .main import build_analysis, parse_input_documents, save_analysis, save_presentation
from .models import AnalysisOutput, Dependency, Document, GraphSummary, Slide
from .parser import DocumentParser
from .pptx_exporter import PptxExporter
from .slide_generator import SlideGenerator

__all__ = [
    "AnalysisOutput",
    "Dependency",
    "DependencyAnalyzer",
    "Document",
    "DocumentParser",
    "GraphSummary",
    "PptxExporter",
    "Slide",
    "SlideGenerator",
    "build_analysis",
    "parse_input_documents",
    "save_analysis",
    "save_presentation",
]
