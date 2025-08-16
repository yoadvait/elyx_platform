# Elyx Hackathon Implementation Guide

## Project Overview

Transform your existing group chat + logging system into a comprehensive Elyx-style health intervention platform that demonstrates advanced AI orchestration, decision traceability, and longitudinal health journey visualization.

## Core Implementation Strategy

### Phase 1: Foundation (Weekend 1) - 20-25 hours

#### 1. Enhanced Agent System (8-12 hours)
**Objective**: Transform generic agent responses into role-specific, SLA-tracked interactions

**Implementation**:
```javascript
// Agent role definitions
const AGENT_ROLES = {
  CONCIERGE: {
    name: 'Ruby',
    responsibilities: ['logistics', 'scheduling', 'coordination', 'friction_removal'],
    responseStyle: 'empathetic, organized, proactive',
    slaTarget: 2 // hours for standard responses
  },
  MEDICAL_STRATEGIST: {
    name: 'Dr. Warren',
    responsibilities: ['medical_decisions', 'lab_interpretation', 'clinical_strategy'],
    responseStyle: 'authoritative, precise, scientific',
    slaTarget: 4
  },
  PERFORMANCE_SCIENTIST: {
    name: 'Advik',
    responsibilities: ['wearable_data', 'exercise_protocols', 'recovery_analysis'],
    responseStyle: 'analytical, data-driven, experimental',
    slaTarget: 3
  }
  // Continue for all 6 roles from Elyx sample
};

// Message routing logic
function routeMessage(message, memberContext) {
  const urgency = detectUrgency(message.content);
  const primaryAgent = determineResponsibleAgent(message.content, message.tags);
  
  return {
    assignedAgent: primaryAgent,
    urgencyLevel: urgency,
    slaDeadline: calculateSLA(urgency, primaryAgent),
    escalationRules: defineEscalation(urgency, primaryAgent)
  };
}
```

**Key Features**:
- Role-based message routing using NLP keywords and context
- SLA tracking with automated escalation to Concierge Lead
- Response time analytics per agent type
- Urgency detection (illness, dissatisfaction, logistics)

#### 2. Why-Traceability Graph (6-10 hours)
**Objective**: Create decision provenance from every plan back to evidence and conversations

**Implementation**:
```javascript
// Decision graph structure
const DecisionGraph = {
  decisions: [{
    id: 'decision_001',
    type: 'medication_recommendation',
    content: 'Start magnesium threonate 400mg before bed',
    timestamp: '2025-08-15T22:30:00Z',
    responsibleAgent: 'Dr. Warren',
    evidenceNodes: ['evidence_001', 'evidence_002'],
    sourceMessages: ['msg_145', 'msg_147'],
    rationale: 'Based on poor sleep latency (25min avg) and member preference for natural interventions'
  }],
  evidence: [{
    id: 'evidence_001',
    type: 'biomarker_data',
    source: 'whoop_sleep_analysis',
    data: { sleepLatency: 25, deepSleep: 40, disturbances: 12 },
    timestamp: '2025-08-14T07:00:00Z'
  }],
  messages: [{
    id: 'msg_145',
    content: 'Slept through the night for the first time in months. Coincidence?',
    author: 'member',
    timestamp: '2025-08-15T08:30:00Z'
  }]
};

// Why-traceability API
app.get('/api/decisions/:id/why', (req, res) => {
  const decision = findDecision(req.params.id);
  const provenance = {
    decision: decision,
    evidence: decision.evidenceNodes.map(id => findEvidence(id)),
    conversations: decision.sourceMessages.map(id => findMessage(id)),
    timeline: constructTimelineView(decision)
  };
  res.json(provenance);
});
```

### Phase 2: Core Features (Weekend 2) - 18-22 hours

#### 3. Episode Management System (10-15 hours)
**Objective**: Structure all interactions as episodes with clear triggers, outcomes, and state transitions

**Implementation**:
```javascript
// Episode schema
const EpisodeSchema = {
  id: String,
  title: String, // "Member Dissatisfaction - Service Feedback"
  triggerEvent: {
    type: String, // 'member_initiated', 'system_alert', 'scheduled_checkup'
    description: String,
    timestamp: Date,
    triggerActor: String // 'member', 'agent_name', 'system'
  },
  frictionPoints: [{
    category: String, // 'communication', 'accessibility', 'scheduling'
    description: String,
    severity: Number, // 1-5
    resolutionAction: String
  }],
  interventions: [{
    action: String,
    responsibleAgent: String,
    timestamp: Date,
    outcome: String
  }],
  memberStateChange: {
    before: String, // 'frustrated', 'engaged', 'optimizing'
    after: String,
    confidence: Number
  },
  metrics: {
    responseTime: Number, // minutes to first response
    resolutionTime: Number, // hours to episode closure
    satisfactionScore: Number
  },
  status: String // 'open', 'in_progress', 'resolved', 'escalated'
};

// Episode state machine
class EpisodeManager {
  createEpisode(trigger, memberContext) {
    const episode = new Episode({
      trigger,
      memberState: this.assessMemberState(memberContext),
      priorityLevel: this.calculatePriority(trigger, memberContext)
    });
    
    return this.routeToAgent(episode);
  }
  
  updateEpisode(episodeId, intervention) {
    const episode = this.findEpisode(episodeId);
    episode.interventions.push(intervention);
    
    if (this.shouldEscalate(episode)) {
      return this.escalateToLead(episode);
    }
    
    return episode;
  }
}
```

#### 4. Experiment Engine (8-12 hours)
**Objective**: Transform ad-hoc suggestions into structured experiments with measurable outcomes

**Implementation**:
```javascript
// Experiment templates
const ExperimentTemplates = {
  SLEEP_OPTIMIZATION: {
    hypothesis: 'Blue light blocking glasses after 4pm will improve deep sleep quality',
    protocol: {
      intervention: 'Wear blue-light glasses during evening screen time',
      duration: '2 weeks',
      measurements: ['sleep_latency', 'deep_sleep_minutes', 'sleep_disturbances'],
      adherence_tracking: 'daily_checklist'
    },
    successCriteria: {
      primary: 'deep_sleep_increase > 20%',
      secondary: 'sleep_latency_decrease > 30%'
    }
  },
  NUTRITION_INTERVENTION: {
    hypothesis: 'Soaking legumes overnight will reduce digestive issues',
    protocol: {
      intervention: 'Chef soaks all legumes 12+ hours before cooking',
      duration: '1 week',
      measurements: ['bloating_score', 'digestive_comfort'],
      adherence_tracking: 'chef_confirmation'
    }
  }
};

// Experiment workflow
class ExperimentEngine {
  proposeExperiment(memberIssue, agentContext) {
    const template = this.selectTemplate(memberIssue);
    const customizedExperiment = this.customizeForMember(template, memberIssue);
    
    return {
      experiment: customizedExperiment,
      rationale: this.generateRationale(customizedExperiment, memberIssue),
      expectedOutcome: this.predictOutcome(customizedExperiment)
    };
  }
  
  trackExperiment(experimentId, dataPoint) {
    const experiment = this.findExperiment(experimentId);
    experiment.measurements.push(dataPoint);
    
    if (this.isExperimentComplete(experiment)) {
      return this.analyzeResults(experiment);
    }
  }
}
```

### Phase 3: Advanced Features (Final Weekend) - 20-25 hours

#### 5. Journey Visualization (12-18 hours)
**Objective**: Create interactive timeline showing episodes, state changes, and data correlations

**Implementation**:
```jsx
// React component for journey timeline
import { Timeline, TimelineItem } from '@material-ui/lab';
import { Zoom, PanZoom } from 'd3-zoom';

const JourneyVisualization = ({ memberData, episodes, experiments }) => {
  const [selectedTimeframe, setSelectedTimeframe] = useState('8_months');
  const [focusEpisode, setFocusEpisode] = useState(null);

  const renderTimeline = () => (
    <Timeline>
      {episodes.map(episode => (
        <TimelineItem key={episode.id}>
          <EpisodeMarker 
            episode={episode}
            frictionLevel={episode.frictionPoints.length}
            onClick={() => setFocusEpisode(episode)}
          />
          <EpisodeDetails episode={episode} />
        </TimelineItem>
      ))}
    </Timeline>
  );

  const renderDataOverlays = () => (
    <DataOverlayChart>
      {memberData.biomarkers.map(dataPoint => (
        <DataPoint
          key={dataPoint.id}
          timestamp={dataPoint.timestamp}
          value={dataPoint.value}
          type={dataPoint.type}
          linkedEpisodes={findRelatedEpisodes(dataPoint)}
        />
      ))}
    </DataOverlayChart>
  );

  return (
    <div className="journey-visualization">
      <TimeframeSelector onChange={setSelectedTimeframe} />
      <ZoomableTimeline>
        {renderTimeline()}
        {renderDataOverlays()}
      </ZoomableTimeline>
      {focusEpisode && (
        <EpisodeDetailPanel 
          episode={focusEpisode}
          onShowWhy={() => showDecisionProvenance(focusEpisode)}
        />
      )}
    </div>
  );
};
```

#### 6. Mock Data Integration (6-10 hours)
**Objective**: Generate realistic health data streams that correlate with your demo narrative

**Implementation**:
```python
# Mock data generator
import json
import random
from datetime import datetime, timedelta

class HealthDataGenerator:
    def __init__(self, member_profile):
        self.profile = member_profile
        self.baseline_hrv = 42  # From Elyx sample
        self.current_date = datetime(2025, 1, 15)
        
    def generate_whoop_data(self, days=240):  # 8 months
        data = []
        hrv_trend = 0  # Gradual improvement over time
        
        for i in range(days):
            date = self.current_date + timedelta(days=i)
            
            # Simulate interventions affecting data
            if i > 30:  # After magnesium intervention
                hrv_trend += 0.1
            if i > 60:  # After sleep protocol
                hrv_trend += 0.15
            if 45 <= i <= 52:  # Illness episode
                hrv_trend -= 5
                
            data.append({
                'date': date.isoformat(),
                'hrv': max(25, self.baseline_hrv + hrv_trend + random.uniform(-8, 8)),
                'recovery': self.calculate_recovery(hrv_trend, i),
                'sleep_performance': self.calculate_sleep(i),
                'strain': random.uniform(8, 18)
            })
            
        return data
    
    def generate_cgm_data(self, start_day=120):  # CGM introduced later
        """Generate glucose data with meal correlations"""
        data = []
        for i in range(120):  # 4 months of CGM
            date = self.current_date + timedelta(days=start_day + i)
            
            # Simulate meal experiments from Elyx sample
            meals = self.simulate_daily_meals(i)
            glucose_data = self.simulate_glucose_response(meals, i)
            
            data.extend(glucose_data)
            
        return data

# WebSocket integration for real-time data
class DataStreamer:
    def __init__(self, socket_io):
        self.io = socket_io
        self.generator = HealthDataGenerator(member_profile)
        
    def stream_historical_data(self, member_id, speed_multiplier=1000):
        """Stream 8 months of data in compressed time for demo"""
        data = self.generator.generate_complete_dataset()
        
        for data_point in data:
            self.io.emit('health_data_update', {
                'member_id': member_id,
                'data': data_point,
                'timestamp': data_point['timestamp']
            })
            time.sleep(0.1 / speed_multiplier)  # Compressed timeline
```

## Technical Architecture Recommendations

### Database Schema Design
```javascript
// MongoDB collections structure
const Collections = {
  members: {
    profile: Object,
    preferences: Object,
    currentState: String,
    constraints: Object  // travel, time availability, etc.
  },
  
  messages: {
    content: String,
    author: String, // member or agent name
    timestamp: Date,
    urgency: Number,
    tags: [String],
    responseTime: Number,
    episodeId: String
  },
  
  episodes: {
    // Full episode schema as defined above
  },
  
  decisions: {
    // Decision graph structure as defined above
  },
  
  experiments: {
    template: String,
    hypothesis: String,
    protocol: Object,
    measurements: [Object],
    outcome: String,
    success: Boolean
  },
  
  health_data: {
    memberId: String,
    source: String, // 'whoop', 'cgm', 'labs'
    type: String,
    value: Number,
    timestamp: Date,
    synthetic: Boolean  // Mark as demo data
  }
};
```

### API Endpoint Structure
```javascript
// Core API routes
const apiRoutes = {
  // Agent system
  'POST /api/messages': 'Send message, trigger agent routing',
  'GET /api/agents/:id/performance': 'SLA metrics, response times',
  'POST /api/escalate/:episodeId': 'Manual escalation to lead',
  
  // Episode management
  'GET /api/episodes': 'List episodes with filters',
  'POST /api/episodes': 'Create new episode',
  'PUT /api/episodes/:id': 'Update episode status/interventions',
  'GET /api/episodes/:id/timeline': 'Detailed episode progression',
  
  // Decision traceability
  'GET /api/decisions/:id/why': 'Full provenance chain',
  'GET /api/plans/:version/diff': 'Plan version comparison',
  'POST /api/decisions/:id/feedback': 'Member acceptance/rejection',
  
  // Experiments
  'POST /api/experiments/propose': 'Create experiment from member issue',
  'PUT /api/experiments/:id/data': 'Log experiment measurement',
  'GET /api/experiments/results': 'Successful interventions list',
  
  // Journey visualization
  'GET /api/members/:id/journey': 'Complete timeline data',
  'GET /api/members/:id/state-history': 'Member state progressions',
  'GET /api/data-correlations': 'Health data matched to episodes'
};
```

## Demo Narrative Flow

### 8-Month Journey Highlights
1. **Month 1**: Onboarding frustration → Whoop data revelation → First targeted intervention
2. **Month 2**: Magnesium experiment success → Member engagement increase
3. **Month 3**: Service dissatisfaction episode → Process improvement → Trust rebuilding  
4. **Month 4**: Illness setback → Comprehensive monitoring → Recovery tracking
5. **Month 5-6**: CGM insights → Nutrition optimization → Travel protocol success
6. **Month 7-8**: Long-term strategy → ApoB reduction → Member advocacy

### Key Demo Moments
- **Why-Traceability**: Click on "Start magnesium threonate" → see sleep data + conversation + agent reasoning
- **Episode Management**: Dissatisfaction episode showing friction categorization and resolution actions
- **Experiment Success**: CGM sushi experiment with before/after glucose curves
- **State Progression**: Visual timeline showing "frustrated" → "engaged" → "advocating" member states

## Success Metrics for Hackathon Judges

### Technical Innovation
- **Decision Provenance**: Every plan item traceable to conversations and data
- **Multi-Agent Orchestration**: Realistic role-based interactions with SLA monitoring
- **Experiment Framework**: Structured hypothesis-testing with outcome tracking

### User Experience Excellence  
- **Journey Visualization**: Interactive timeline with drill-down capability
- **Friction Analysis**: Systematic categorization and resolution of member issues
- **Context Awareness**: Agents remember constraints and preferences

### Healthcare Domain Expertise
- **Realistic Scenarios**: Based directly on Elyx sample interactions
- **Clinical Decision Making**: Evidence-based recommendations with uncertainty acknowledgment  
- **Longitudinal Optimization**: Multi-month strategy with measurable health outcomes

This implementation approach transforms your existing foundation into a comprehensive demonstration of advanced healthcare AI orchestration, positioning you to excel in the hackathon by showing both technical sophistication and deep understanding of the healthcare member journey.