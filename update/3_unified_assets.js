// Merges: script.js + programmer.js + Cosmic JS logic

class CosmicTheme {
  static applyBackground() {
    document.body.classList.add('cosmic-theme')
    this.createStars()
  }
  
  static createStars() {
    const container = document.createElement('div')
    container.id = 'cosmic-bg'
    document.body.prepend(container)
    
    for (let i = 0; i < 200; i++) {
      const star = document.createElement('div')
      star.className = 'cosmic-star'
      star.style.cssText = `
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        width: ${Math.random() * 3}px;
        height: ${Math.random() * 3}px;
        animation-delay: ${Math.random() * 4}s;
      `
      container.appendChild(star)
    }
  }
}

class CommandManager {
  static async toggle(command, status) {
    const response = await fetch(`/api/toggle/${command}`, {
      method: 'POST',
      body: JSON.stringify({ status })
    })
    return response.json()
  }
}

// Unified initialization
document.addEventListener('DOMContentLoaded', () => {
  CosmicTheme.applyBackground()
  
  // Initialize all command toggles
  document.querySelectorAll('.command-toggle').forEach(toggle => {
    toggle.addEventListener('change', (e) => {
      CommandManager.toggle(
        e.target.dataset.command, 
        e.target.checked
      )
    })
  })
})