<template>
  <!-- Merges: HelpPanel.vue + ServiceControlPanel.vue + ConflictResolver.vue -->
  <div class="universal-component">
    <!-- Dynamic renderer for different modes -->
    <component :is="currentView" :data="componentData"></component>
    
    <!-- Shared UI Elements -->
    <div class="universal-controls">
      <button @click="refreshData">Refresh</button>
      <button @click="toggleHelpMode">Help Mode</button>
    </div>
  </div>
</template>

<script>
import CommandHelp from './CommandHelp.vue'
import ServiceControl from './ServiceControl.vue'
import ConflictResolver from './ConflictResolver.vue'

export default {
  components: { CommandHelp, ServiceControl, ConflictResolver },
  
  data() {
    return {
      currentView: 'CommandHelp',
      componentData: null,
      helpMode: false
    }
  },
  
  methods: {
    async refreshData() {
      // Unified data loader
      const [commands, services] = await Promise.all([
        fetch('/api/commands').then(r => r.json()),
        fetch('/api/services').then(r => r.json())
      ])
      
      this.componentData = { commands, services }
    },
    
    toggleHelpMode() {
      this.helpMode = !this.helpMode
      this.currentView = this.helpMode ? 'CommandHelp' : 'ServiceControl'
    },
    
    // Merged from ConflictResolver.vue
    resolveConflict(resolution) {
      this.$emit('resolve', resolution)
    }
  }
}
</script>