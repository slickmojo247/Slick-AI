flowchart LR
    A[VSCode] <--> B[SLICK AI]
    C[Web Interface] <--> B
    B --> D[Telegram Bot]
    D --> E[OpenAI\nAPI]
    D --> F[DeepSeek\nAPI]
    G[User] --> A
    G --> C
    G --> B
    H[WO Mic\n(Phone)] -->|Port 8125| I[Windows\nComputer]
    I --> B[SLICK AI]
    G --> H
    
    style A fill:#248aff,stroke:#1a6fbb
    style C fill:#ff8c42,stroke:#cc6f35
    style B fill:#7e57c2,stroke:#6445a0
    style D fill:#26a69a,stroke:#1d7f74
    style E fill:#66bb6a,stroke:#4c9e50
    style F fill:#66bb6a,stroke:#4c9e50
    style G fill:#ff7043,stroke:#cc5935
    style H fill:#ab47bc,stroke:#8e24aa
    style I fill:#42a5f5,stroke:#1e88e5

    sequenceDiagram
    participant User
    participant Phone
    participant Windows
    participant SLICK_AI
    participant Telegram
    participant OpenAI
    
    User->>Phone: Speaks command
    Phone->>Windows: Streams audio (port 8125)
    Windows->>SLICK_AI: Sends transcribed text
    SLICK_AI->>Telegram: Forwards query if needed
    Telegram->>OpenAI: Processes with API key
    OpenAI-->>Telegram: Returns response
    Telegram-->>SLICK_AI: Forwards response
    SLICK_AI-->>Windows: May generate audio response
    Windows-->>Phone: Plays response if needed

    flowchart LR
    A[VSCode] <--> B[SLICK AI]
    C[Web Interface] <--> B
    H[WO Mic] -->|8125| I[Windows]
    I --> B
    
    subgraph AI Processing
        B --> D[API Orchestrator]
        D -->|API Key 1| E[OpenAI]
        D -->|API Key 2| F[DeepSeek]
        E --> G[Response Blender]
        F --> G
        G --> B
    end
    
    D --> T[Telegram Bot]
    T --> E & F
    
    style E fill:#66bb6a,stroke:#4c9e50
    style F fill:#66bb6a,stroke:#4c9e50
    style G fill:#ffca28,stroke:#ffa000
    style D fill:#26a69a,stroke:#1d7f74

    sequenceDiagram
    SLICK_AI->>Orchestrator: User Query
    Orchestrator->>OpenAI: Primary Request (Key1)
    Orchestrator->>DeepSeek: Complementary Request (Key2)
    OpenAI-->>Blender: Base Response
    DeepSeek-->>Blender: Supporting Data
    Blender->>SLICK_AI: Enhanced Final Response

    