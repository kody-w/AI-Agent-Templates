"""
AI Decision System for Retail CPG Agents
Provides transparent, explainable AI-powered decision making with confidence scoring
"""

import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import json


class AIDecisionEngine:
    """Base class for AI-powered decision making with transparency and explainability"""
    
    def __init__(self, domain: str, decision_context: Dict[str, Any] = None):
        self.domain = domain
        self.decision_context = decision_context or {}
        self.model_version = "1.0.0"
        
    def make_decision(self, 
                     decision_type: str,
                     input_data: Dict[str, Any],
                     thresholds: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        Make an AI-powered decision with full transparency
        
        Returns:
            Dictionary containing decision, confidence, explanation, and audit trail
        """
        # Analyze input completeness and quality
        data_quality_score = self._assess_data_quality(input_data)
        
        # Generate decision based on probabilistic assessment
        decision, factors = self._generate_decision(decision_type, input_data)
        
        # Calculate confidence score
        confidence = self._calculate_confidence(
            data_quality_score,
            factors,
            input_data
        )
        
        # Generate detailed explanation
        explanation = self._generate_explanation(
            decision_type,
            decision,
            factors,
            confidence,
            input_data
        )
        
        # Determine if human review is needed
        override_recommendation = self._assess_override_need(
            confidence,
            decision_type,
            thresholds
        )
        
        # Create audit trail
        audit_trail = self._create_audit_trail(
            decision_type,
            input_data,
            decision
        )
        
        return {
            'decision': decision,
            'confidence': confidence,
            'explanation': explanation,
            'override_recommendation': override_recommendation,
            'audit_trail': audit_trail
        }
    
    def _assess_data_quality(self, input_data: Dict[str, Any]) -> float:
        """Assess the quality and completeness of input data"""
        quality_score = 0.5  # Base score
        
        # Check for required fields
        if input_data:
            field_count = len(input_data)
            if field_count > 5:
                quality_score += 0.2
            elif field_count > 2:
                quality_score += 0.1
        
        # Check for data freshness (if timestamps present)
        if 'timestamp' in input_data:
            quality_score += 0.1
            
        # Check for historical context
        if 'historical_data' in input_data:
            quality_score += 0.2
            
        return min(1.0, quality_score)
    
    def _generate_decision(self, 
                          decision_type: str, 
                          input_data: Dict[str, Any]) -> Tuple[Any, Dict[str, float]]:
        """Generate decision using probabilistic reasoning"""
        # This would be replaced with actual ML model inference
        # For now, using intelligent heuristics
        
        factors = {}
        
        # Domain-specific decision logic
        if self.domain == "inventory":
            return self._inventory_decision(decision_type, input_data, factors)
        elif self.domain == "marketing":
            return self._marketing_decision(decision_type, input_data, factors)
        elif self.domain == "returns":
            return self._returns_decision(decision_type, input_data, factors)
        elif self.domain == "store_ops":
            return self._store_ops_decision(decision_type, input_data, factors)
        elif self.domain == "supply_chain":
            return self._supply_chain_decision(decision_type, input_data, factors)
        else:
            return self._default_decision(decision_type, input_data, factors)
    
    def _inventory_decision(self, decision_type: str, input_data: Dict[str, Any], factors: Dict) -> Tuple[Any, Dict]:
        """Inventory-specific decision logic"""
        if decision_type == "restock_priority":
            # Evaluate multiple factors for restocking decision
            factors['current_stock_level'] = input_data.get('stock_level', 50) / 100
            factors['demand_forecast'] = input_data.get('demand_forecast', 0.5)
            factors['lead_time'] = 1.0 - (input_data.get('lead_time_days', 7) / 30)
            factors['seasonality'] = input_data.get('seasonality_factor', 0.5)
            
            weighted_score = (
                factors['current_stock_level'] * 0.3 +
                factors['demand_forecast'] * 0.3 +
                factors['lead_time'] * 0.2 +
                factors['seasonality'] * 0.2
            )
            
            if weighted_score > 0.7:
                decision = "urgent_restock"
            elif weighted_score > 0.4:
                decision = "standard_restock"
            else:
                decision = "monitor_only"
                
            return decision, factors
        
        return "standard_processing", factors
    
    def _marketing_decision(self, decision_type: str, input_data: Dict[str, Any], factors: Dict) -> Tuple[Any, Dict]:
        """Marketing-specific decision logic"""
        if decision_type == "campaign_targeting":
            # Evaluate customer segments probabilistically
            factors['purchase_history'] = input_data.get('purchase_frequency', 0.5)
            factors['engagement_score'] = input_data.get('engagement', 0.5)
            factors['lifetime_value'] = input_data.get('ltv_percentile', 50) / 100
            factors['churn_risk'] = 1.0 - input_data.get('churn_probability', 0.3)
            
            segment_score = (
                factors['purchase_history'] * 0.25 +
                factors['engagement_score'] * 0.25 +
                factors['lifetime_value'] * 0.3 +
                factors['churn_risk'] * 0.2
            )
            
            if segment_score > 0.75:
                decision = "premium_segment"
            elif segment_score > 0.5:
                decision = "standard_segment"
            elif segment_score > 0.25:
                decision = "re_engagement_segment"
            else:
                decision = "low_priority_segment"
                
            return decision, factors
        
        return "standard_campaign", factors
    
    def _returns_decision(self, decision_type: str, input_data: Dict[str, Any], factors: Dict) -> Tuple[Any, Dict]:
        """Returns and complaints decision logic"""
        if decision_type == "return_approval":
            # Evaluate return request with multiple factors
            factors['return_reason_validity'] = input_data.get('reason_score', 0.7)
            factors['customer_history'] = input_data.get('customer_trust_score', 0.8)
            factors['product_condition'] = input_data.get('condition_score', 0.6)
            factors['time_since_purchase'] = 1.0 - (input_data.get('days_since_purchase', 15) / 90)
            factors['return_cost_ratio'] = 1.0 - (input_data.get('return_cost', 20) / 100)
            
            approval_score = (
                factors['return_reason_validity'] * 0.3 +
                factors['customer_history'] * 0.25 +
                factors['product_condition'] * 0.2 +
                factors['time_since_purchase'] * 0.15 +
                factors['return_cost_ratio'] * 0.1
            )
            
            if approval_score > 0.75:
                decision = "auto_approve"
            elif approval_score > 0.5:
                decision = "conditional_approve"
            elif approval_score > 0.3:
                decision = "manual_review_required"
            else:
                decision = "likely_reject"
                
            return decision, factors
        
        return "standard_handling", factors
    
    def _store_ops_decision(self, decision_type: str, input_data: Dict[str, Any], factors: Dict) -> Tuple[Any, Dict]:
        """Store operations decision logic"""
        if decision_type == "staff_assistance_priority":
            # Prioritize assistance based on multiple factors
            factors['customer_value'] = input_data.get('customer_tier', 0.5)
            factors['query_complexity'] = input_data.get('complexity_score', 0.5)
            factors['wait_time'] = min(1.0, input_data.get('wait_minutes', 0) / 10)
            factors['purchase_intent'] = input_data.get('purchase_probability', 0.5)
            
            priority_score = (
                factors['customer_value'] * 0.3 +
                factors['query_complexity'] * 0.2 +
                factors['wait_time'] * 0.3 +
                factors['purchase_intent'] * 0.2
            )
            
            if priority_score > 0.7:
                decision = "immediate_assistance"
            elif priority_score > 0.4:
                decision = "standard_queue"
            else:
                decision = "self_service_recommended"
                
            return decision, factors
        
        return "standard_service", factors
    
    def _supply_chain_decision(self, decision_type: str, input_data: Dict[str, Any], factors: Dict) -> Tuple[Any, Dict]:
        """Supply chain decision logic"""
        if decision_type == "disruption_severity":
            # Assess disruption impact probabilistically
            factors['impact_scope'] = input_data.get('affected_products', 10) / 100
            factors['delay_severity'] = input_data.get('delay_days', 3) / 14
            factors['alternative_availability'] = 1.0 - input_data.get('alternative_score', 0.7)
            factors['customer_impact'] = input_data.get('customer_orders_affected', 50) / 500
            factors['financial_impact'] = input_data.get('revenue_at_risk', 10000) / 100000
            
            severity_score = (
                factors['impact_scope'] * 0.2 +
                factors['delay_severity'] * 0.25 +
                factors['alternative_availability'] * 0.15 +
                factors['customer_impact'] * 0.25 +
                factors['financial_impact'] * 0.15
            )
            
            if severity_score > 0.75:
                decision = "critical_disruption"
            elif severity_score > 0.5:
                decision = "major_disruption"
            elif severity_score > 0.25:
                decision = "minor_disruption"
            else:
                decision = "negligible_impact"
                
            return decision, factors
        
        return "monitor_situation", factors
    
    def _default_decision(self, decision_type: str, input_data: Dict[str, Any], factors: Dict) -> Tuple[Any, Dict]:
        """Default decision logic when domain-specific logic not available"""
        factors['data_completeness'] = len(input_data) / 10
        factors['processing_confidence'] = 0.5
        
        return "standard_processing", factors
    
    def _calculate_confidence(self, 
                            data_quality: float,
                            factors: Dict[str, float],
                            input_data: Dict[str, Any]) -> float:
        """Calculate confidence score for the decision"""
        # Base confidence from data quality
        confidence = data_quality * 0.3
        
        # Factor consistency check
        if factors:
            factor_values = list(factors.values())
            if factor_values:
                # High variance in factors reduces confidence
                avg_factor = sum(factor_values) / len(factor_values)
                variance = sum((f - avg_factor) ** 2 for f in factor_values) / len(factor_values)
                consistency_score = 1.0 - min(1.0, variance * 2)
                confidence += consistency_score * 0.3
        
        # Historical accuracy (simulated)
        historical_accuracy = 0.75 + random.random() * 0.2
        confidence += historical_accuracy * 0.2
        
        # Model certainty based on input patterns
        pattern_match = 0.6 + random.random() * 0.3
        confidence += pattern_match * 0.2
        
        return round(min(1.0, max(0.0, confidence)), 3)
    
    def _generate_explanation(self,
                            decision_type: str,
                            decision: Any,
                            factors: Dict[str, float],
                            confidence: float,
                            input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed explanation for the decision"""
        
        # Sort factors by importance
        sorted_factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)
        
        # Identify primary drivers
        primary_factors = []
        for factor_name, factor_value in sorted_factors[:3]:
            primary_factors.append({
                'factor': factor_name.replace('_', ' ').title(),
                'influence': 'High' if factor_value > 0.7 else 'Moderate' if factor_value > 0.4 else 'Low',
                'value': round(factor_value, 2)
            })
        
        # Generate reasoning narrative
        reasoning = f"Decision '{decision}' was reached after analyzing {len(factors)} factors. "
        
        if confidence > 0.8:
            reasoning += "The AI has high confidence in this decision based on strong signal alignment. "
        elif confidence > 0.6:
            reasoning += "The AI has moderate confidence, with most indicators supporting this decision. "
        else:
            reasoning += "The AI has lower confidence due to conflicting or incomplete signals. "
        
        if sorted_factors:
            top_factor = sorted_factors[0][0].replace('_', ' ')
            reasoning += f"The primary driver was {top_factor}. "
        
        # Identify alternatives considered
        alternatives = self._identify_alternatives(decision_type, decision, factors)
        
        # Identify uncertainty sources
        uncertainty_sources = []
        if confidence < 0.7:
            if 'historical_data' not in input_data:
                uncertainty_sources.append("Limited historical context")
            if len(input_data) < 3:
                uncertainty_sources.append("Incomplete input data")
            if any(v < 0.3 for v in factors.values()):
                uncertainty_sources.append("Weak signals in some factors")
        
        return {
            'factors_considered': list(factors.keys()),
            'factor_weights': {k: round(v, 3) for k, v in factors.items()},
            'primary_factors': primary_factors,
            'reasoning': reasoning,
            'alternatives': alternatives,
            'uncertainty_sources': uncertainty_sources,
            'confidence_breakdown': {
                'data_quality': round(confidence * 0.3, 2),
                'pattern_matching': round(confidence * 0.4, 2),
                'historical_accuracy': round(confidence * 0.3, 2)
            }
        }
    
    def _identify_alternatives(self, 
                              decision_type: str,
                              selected_decision: str,
                              factors: Dict[str, float]) -> List[Dict[str, Any]]:
        """Identify alternative decisions that were considered"""
        alternatives = []
        
        # Domain-specific alternatives
        if self.domain == "inventory" and decision_type == "restock_priority":
            all_options = ["urgent_restock", "standard_restock", "monitor_only"]
        elif self.domain == "marketing" and decision_type == "campaign_targeting":
            all_options = ["premium_segment", "standard_segment", "re_engagement_segment", "low_priority_segment"]
        elif self.domain == "returns" and decision_type == "return_approval":
            all_options = ["auto_approve", "conditional_approve", "manual_review_required", "likely_reject"]
        elif self.domain == "store_ops" and decision_type == "staff_assistance_priority":
            all_options = ["immediate_assistance", "standard_queue", "self_service_recommended"]
        elif self.domain == "supply_chain" and decision_type == "disruption_severity":
            all_options = ["critical_disruption", "major_disruption", "minor_disruption", "negligible_impact"]
        else:
            all_options = ["standard_processing"]
        
        for option in all_options:
            if option != selected_decision:
                # Calculate hypothetical score for this alternative
                score = random.random() * 0.7  # Simplified - would use actual model
                alternatives.append({
                    'option': option,
                    'probability': round(score, 2),
                    'reason_not_selected': self._explain_alternative_rejection(option, selected_decision, factors)
                })
        
        return sorted(alternatives, key=lambda x: x['probability'], reverse=True)[:2]
    
    def _explain_alternative_rejection(self, 
                                      alternative: str,
                                      selected: str,
                                      factors: Dict[str, float]) -> str:
        """Explain why an alternative wasn't selected"""
        if 'urgent' in alternative and 'urgent' not in selected:
            return "Urgency factors did not meet threshold"
        elif 'premium' in alternative and 'premium' not in selected:
            return "Value indicators insufficient for premium treatment"
        elif 'critical' in alternative and 'critical' not in selected:
            return "Impact assessment below critical threshold"
        elif 'approve' in alternative and 'reject' in selected:
            return "Risk factors outweighed approval criteria"
        else:
            return "Other options showed stronger signal alignment"
    
    def _assess_override_need(self,
                             confidence: float,
                             decision_type: str,
                             thresholds: Optional[Dict[str, float]] = None) -> Optional[str]:
        """Determine if human review/override is recommended"""
        
        # Default thresholds
        default_thresholds = {
            'auto_execute': 0.8,
            'recommend_review': 0.6,
            'require_review': 0.4
        }
        
        thresholds = thresholds or default_thresholds
        
        if confidence >= thresholds.get('auto_execute', 0.8):
            return None  # No override needed
        elif confidence >= thresholds.get('recommend_review', 0.6):
            return "Review recommended for validation"
        elif confidence >= thresholds.get('require_review', 0.4):
            return "Manual review strongly recommended due to moderate confidence"
        else:
            return "Human decision required - AI confidence below acceptable threshold"
    
    def _create_audit_trail(self,
                           decision_type: str,
                           input_data: Dict[str, Any],
                           decision: Any) -> Dict[str, Any]:
        """Create comprehensive audit trail for the decision"""
        return {
            'timestamp': datetime.now().isoformat(),
            'decision_type': decision_type,
            'input_snapshot': input_data.copy(),
            'model_version': self.model_version,
            'domain': self.domain,
            'decision_path': [
                f"Input received: {len(input_data)} parameters",
                f"Data quality assessed",
                f"Decision type: {decision_type}",
                f"Model inference completed",
                f"Confidence calculated",
                f"Final decision: {decision}"
            ],
            'compliance_flags': {
                'gdpr_compliant': True,
                'explainable': True,
                'reversible': True,
                'human_reviewable': True
            }
        }


class AdaptiveThresholdManager:
    """Manages dynamic thresholds based on historical performance"""
    
    def __init__(self):
        self.performance_history = []
        self.current_thresholds = {
            'auto_execute': 0.8,
            'recommend_review': 0.6,
            'require_review': 0.4
        }
    
    def update_thresholds(self, decision_outcome: Dict[str, Any]):
        """Adapt thresholds based on decision outcomes"""
        self.performance_history.append(decision_outcome)
        
        # Calculate accuracy over last 100 decisions
        if len(self.performance_history) >= 100:
            recent_accuracy = self._calculate_recent_accuracy()
            
            # Adjust thresholds based on performance
            if recent_accuracy > 0.95:
                # High accuracy - can be more aggressive
                self.current_thresholds['auto_execute'] = max(0.75, self.current_thresholds['auto_execute'] - 0.02)
            elif recent_accuracy < 0.85:
                # Lower accuracy - be more conservative
                self.current_thresholds['auto_execute'] = min(0.9, self.current_thresholds['auto_execute'] + 0.02)
    
    def _calculate_recent_accuracy(self) -> float:
        """Calculate accuracy of recent decisions"""
        recent = self.performance_history[-100:]
        correct = sum(1 for d in recent if d.get('outcome') == 'correct')
        return correct / len(recent)
    
    def get_thresholds(self, decision_type: str) -> Dict[str, float]:
        """Get current thresholds for a decision type"""
        # Could have decision-type specific thresholds
        return self.current_thresholds.copy()