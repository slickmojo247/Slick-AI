1. Unified Dashboard Template (web_interface/src/views/FullDashboard.vue)


<template>
  <!-- Merges: DeveloperDashboard.vue + HelpDashboard.vue + Cosmic components -->
  <div class="cosmic-dashboard">
    <!-- Header Section -->
    <header class="cosmic-header">
      <h1>SLICK AI Control Center</h1>
      <div class="connection-status">
        <span :class="['status-dot', connectionStatus]"></span>
        {{ connectionText }}
      </div>
    </header>

    <!-- Main Grid -->
    <div class="cosmic-grid">
      <!-- Command Panel (from Cosmic_back.html) -->
      <section class="command-panel">
        <div class="search-box">
          <input v-model="commandSearch" placeholder="Search commands...">
          <button @click="searchCommands">Search</button>
        </div>
        
        <div class="command-cards">
          <div v-for="cmd in filteredCommands" :key="cmd.name" class="command-card">
            <h3>{{ cmd.name }} <i :class="cmd.icon"></i></h3>
            <p>{{ cmd.description }}</p>
            <label class="cosmic-switch">
              <input type="checkbox" v-model="cmd.status" @change="toggleCommand(cmd)">
              <span class="slider"></span>
            </label>
          </div>
        </div>
      </section>

      <!-- Service Control (from ServiceControlPanel.vue) -->
      <section class="service-panel">
        <h2>Service Matrix</h2>
        <div class="service-grid">
          <div v-for="svc in services" :key="svc.id" class="service-card">
            <div class="service-header">
              <h3>{{ svc.name }}</h3>
              <span :class="['status-badge', svc.status]">{{ svc.status }}</span>
            </div>
            <div class="service-actions">
              <button @click="startService(svc)">Start</button>
              <button @click="stopService(svc)">Stop</button>
              <button @click="showLogs(svc)">Logs</button>
            </div>
          </div>
        </div>
      </section>

      <!-- AI Console (from SLICK.html) -->
      <section class="ai-console">
        <div class="chat-interface">
          <textarea v-model="aiPrompt" placeholder="Ask AI anything..."></textarea>
          <button @click="sendToAI">Submit</button>
          <div class="ai-response" v-html="aiResponse"></div>
        </div>
      </section>
    </div>

    <!-- Help System (from HelpPanel.vue) -->
    <section class="help-system">
      <div class="help-tabs">
        <button v-for="tab in helpTabs" 
                :key="tab.id"
                @click="activeHelpTab = tab.id"
                :class="{active: activeHelpTab === tab.id}">
          {{ tab.name }}
        </button>
      </div>
      
      <div class="help-content">
        <component :is="activeHelpComponent"></component>
      </div>
    </section>
  </div>
</template>

<script>
// Merged functionality from:
// - Cosmic_back.html
// - ServiceControlPanel.vue 
// - SLICK.html
// - HelpPanel.vue

export default {
  data() {
    return {
      // Command system
      commandSearch: '',
      commands: [
        {
          name: 'CURE',
          description: 'System healing command',
          icon: 'fas fa-heart',
          status: true
        },
        {
          name: 'LOOK',
          description: 'Code analysis command', 
          icon: 'fas fa-eye',
          status: false
        }
      ],
      
      // Service system
      services: [
        { id: 1, name: 'slick-controller', status: 'running' },
        { id: 2, name: 'vscode-bridge', status: 'stopped' }
      ],
      
      // AI system
      aiPrompt: '',
      aiResponse: '',
      
      // Help system
      activeHelpTab: 'commands',
      helpTabs: [
        { id: 'commands', name: 'Command Reference' },
        { id: 'services', name: 'Service Docs' },
        { id: 'changes', name: 'Recent Updates' }
      ]
    }
  },
  
  computed: {
    filteredCommands() {
      return this.commands.filter(cmd => 
        cmd.name.toLowerCase().includes(this.commandSearch.toLowerCase()) ||
        cmd.description.toLowerCase().includes(this.commandSearch.toLowerCase())
    ),
    
    activeHelpComponent() {
      return {
        'commands': () => import('./components/CommandHelp.vue'),
        'services': () => import('./components/ServiceHelp.vue'),
        'changes': () => import('./components/ChangeLog.vue')
      }[this.activeHelpTab]
    },
    
    connectionStatus() {
      return this.services.some(s => s.status === 'running') ? 'connected' : 'disconnected'
    },
    
    connectionText() {
      return this.connectionStatus === 'connected' ? 
        'All systems operational' : 
        'Connection issues detected'
    }
  },
  
  methods: {
    // From Cosmic_back.html and cosmic_front.html
    toggleCommand(cmd) {
      fetch(`/api/toggle/${cmd.name}`, { method: 'POST' })
        .then(() => this.$notify(`Command ${cmd.name} ${cmd.status ? 'enabled' : 'disabled'}`))
    },
    
    // From ServiceControlPanel.vue
    startService(svc) {
      fetch(`/api/services/${svc.id}/start`, { method: 'POST' })
        .then(() => svc.status = 'running')
    },
    
    // From SLICK.html
    sendToAI() {
      fetch('/api/ai/query', {
        method: 'POST',
        body: JSON.stringify({ prompt: this.aiPrompt })
      })
      .then(res => res.json())
      .then(data => this.aiResponse = data.response)
    },
    
    // From HelpPanel.vue
    searchCommands() {
      // Unified search logic
    }
  }
}
</script>

<style>
/* Consolidated cosmic theme from all components */
:root {
  --cosmic-primary: #5d8bf4;
  --cosmic-secondary: #00c9ff;
  --cosmic-dark: rgba(20, 20, 50, 0.7);
  --cosmic-border: rgba(93, 139, 244, 0.3);
}

.cosmic-dashboard {
  display: grid;
  grid-template-rows: auto 1fr;
  background: var(--cosmic-dark);
  color: white;
  min-height: 100vh;
}

.command-card, .service-card {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid var(--cosmic-border);
  border-radius: 12px;
  padding: 1rem;
  margin: 0.5rem 0;
}

.cosmic-switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

/* Additional merged styles from all components... */
</style>