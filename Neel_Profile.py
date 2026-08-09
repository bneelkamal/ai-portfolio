from __future__ import annotations

import random

import streamlit as st


st.set_page_config(
    page_title="Neel's Profile | AI Product Manager",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
.block-container {
    max-width: 1180px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(135deg, #eff6ff, #f8fafc);
    border: 1px solid #dbeafe;
    border-radius: 20px;
    padding: 2.4rem;
    margin-bottom: 1.5rem;
}

.eyebrow {
    color: #2563eb;
    font-size: .82rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
}

.hero h1 {
    font-size: 3rem;
    line-height: 1.1;
    color: #0f172a;
    margin: .35rem 0 .7rem;
}

.hero p {
    font-size: 1.15rem;
    color: #475569;
    max-width: 760px;
}

.card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.2rem;
    min-height: 180px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, .04);
}

.card h3 {
    color: #0f172a;
    margin-top: 0;
    font-size: 1.12rem;
}

.card p {
    color: #475569;
    line-height: 1.55;
}

.tag {
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    border-radius: 999px;
    padding: .25rem .55rem;
    margin: .15rem;
    font-size: .8rem;
}

.section-note {
    color: #64748b;
    margin-top: -.45rem;
}
</style>
""",
    unsafe_allow_html=True,
)


with st.sidebar:

    

    

    st.markdown("### A thought for today")

    quotes = [
        "The best products make complexity feel simple.",
        "Responsible AI begins with responsible questions.",
        "Build for usefulness, measure for trust.",
        "Good product decisions connect evidence with empathy.",
        "The future belongs to teams that can turn intelligence into action.",
        "AI creates value when it helps people make better decisions.",
        "Life is about making an impact, not making an income. – Kevin Kruse",
        "Whatever the mind of man can conceive and believe, it can achieve. – Napoleon Hill",
        "Strive not to be a success, but rather to be of value. – Albert Einstein",
        "You miss 100% of the shots you don’t take. – Wayne Gretzky",
        "Every strike brings me closer to the next home run. – Babe Ruth",
        "Definiteness of purpose is the starting point of all achievement. – W. Clement Stone",
        "We become what we think about. – Earl Nightingale",
        "Life is 10% what happens to me and 90% of how I react to it. – Charles Swindoll",
        "The most common way people give up their power is by thinking they don’t have any. – Alice Walker",
        "The mind is everything. What you think you become. – Buddha",
        "The best time to plant a tree was 20 years ago. The second best time is now. – Chinese Proverb",
        "An unexamined life is not worth living. – Socrates",
        "Eighty percent of success is showing up. – Woody Allen",
        "Your time is limited, so don’t waste it living someone else’s life. – Steve Jobs",
        "Winning isn’t everything, but wanting to win is. – Vince Lombardi",
        "I am not a product of my circumstances. I am a product of my decisions. – Stephen Covey",
        "Every child is an artist. The problem is how to remain an artist once he grows up. – Pablo Picasso",
        "You can never cross the ocean until you have the courage to lose sight of the shore. – Christopher Columbus",
        "I’ve learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel. – Maya Angelou",
        "Either you run the day, or the day runs you. – Jim Rohn",
        "Whether you think you can or you think you can’t, you’re right. – Henry Ford",
        "The two most important days in your life are the day you are born and the day you find out why. – Mark Twain",
        "Whatever you can do, or dream you can, begin it. Boldness has genius, power and magic in it. – Johann Wolfgang von Goethe",
        "The best revenge is massive success. – Frank Sinatra",
        "People often say that motivation doesn’t last. Well, neither does bathing. That’s why we recommend it daily. – Zig Ziglar",
        "Life shrinks or expands in proportion to one’s courage. – Anais Nin",
        "If you hear a voice within you say “you cannot paint,” then by all means paint and that voice will be silenced. – Vincent Van Gogh",
        "There is only one way to avoid criticism: do nothing, say nothing, and be nothing. – Aristotle",
        "Ask and it will be given to you; search, and you will find; knock and the door will be opened for you. – Jesus",
        "The only person you are destined to become is the person you decide to be. – Ralph Waldo Emerson",
        "Go confidently in the direction of your dreams. Live the life you have imagined. – Henry David Thoreau",
        "When I stand before God at the end of my life, I would hope that I would not have a single bit of talent left, and could say, I used everything you gave me. – Erma Bombeck",
        "Few things can help an individual more than to place responsibility on him, and to let him know that you trust him. – Booker T. Washington",
        "Certain things catch your eye, but pursue only those that capture the heart. – Ancient Indian Proverb",
        "Believe you can and you’re halfway there. – Theodore Roosevelt",
        "Everything you’ve ever wanted is on the other side of fear. – George Addair",
        "We can easily forgive a child who is afraid of the dark; the real tragedy of life is when men are afraid of the light. – Plato",
        "Teach thy tongue to say, “I do not know,” and thou shalt progress. – Maimonides",
        "Start where you are. Use what you have. Do what you can. – Arthur Ashe",
        "When I was 5 years old, my mother always told me that happiness was the key to life. – John Lennon",
        "Fall seven times and stand up eight. – Japanese Proverb",
        "Everything has beauty, but not everyone can see. – Confucius",
        "How wonderful it is that nobody need wait a single moment before starting to improve the world. – Anne Frank",
        "When one door of happiness closes, another opens, but often we look so long at the closed door that we do not see the one that has been opened for us. – Helen Keller",
        "When I let go of what I am, I become what I might be. – Lao Tzu",
        "Happiness is not something readymade. It comes from your own actions. – Dalai Lama",
        "If you’re offered a seat on a rocket ship, don’t ask what seat! Just get on. – Sheryl Sandberg",
        "First, have a definite, clear practical ideal; a goal, an objective. Second, have the necessary means to achieve your ends; wisdom, money, materials, and methods. Third, adjust all your means to that end. – Aristotle",
        "If the wind will not serve, take to the oars. – Latin Proverb",
        "You can’t fall if you don’t climb. But there’s no joy in living your whole life on the ground. – Unknown",
        "We must believe that we are gifted for something, and that this thing, at whatever cost, must be attained. – Marie Curie",
        "Too many of us are not living our dreams because we are living our fears. – Les Brown",
        "Challenges are what make life interesting and overcoming them is what makes life meaningful. – Joshua J. Marine",
        "If you want to lift yourself up, lift up someone else. – Booker T. Washington",
        "I have been impressed with the urgency of doing. Knowing is not enough; we must apply. Being willing is not enough; we must do. – Leonardo da Vinci",
        "Limitations live only in our minds. But if we use our imaginations, our possibilities become limitless. – Jamie Paolinetti",
        "You take your life in your own hands, and what happens? A terrible thing, no one to blame. – Erica Jong",
        "What’s money? A man is a success if he gets up in the morning and goes to bed at night and in between does what he wants to do. – Bob Dylan",
        "I didn’t fail the test. I just found 100 ways to do it wrong. – Benjamin Franklin",
        "In order to succeed, your desire for success should be greater than your fear of failure. – Bill Cosby",
        "A person who never made a mistake never tried anything new. – Albert Einstein",
        "The person who says it cannot be done should not interrupt the person who is doing it. – Chinese Proverb",
        "There are no traffic jams along the extra mile. – Roger Staubach",
        "It is never too late to be what you might have been. – George Eliot",
        "You become what you believe. – Oprah Winfrey",
        "I would rather die of passion than of boredom. – Vincent van Gogh",
        "A truly rich man is one whose children run into his arms when his hands are empty. – Unknown",
        "It is our choices that show what we truly are, far more than our abilities. – J.K. Rowling",
        "It’s not what you look at that matters, it’s what you see. – Henry David Thoreau",
        "The only way to do great work is to love what you do. – Steve Jobs",
        "Change your thoughts and you change your world. – Norman Vincent Peale",
        "The best way to predict the future is to invent it. – Alan Kay",
        "I have learned over the years that when one’s mind is made up, this diminishes fear. – Rosa Parks",
        "Remember that not getting what you want is sometimes a wonderful stroke of luck. – Dalai Lama",
        "You can’t use up creativity. The more you use, the more you have. – Maya Angelou",
        "Dream big and dare to fail. – Norman Vaughan",
        "Do what you can, where you are, with what you have. – Teddy Roosevelt",
        "If you want to achieve greatness stop asking for permission. – Anonymous",
        "Things work out best for those who make the best of how things work out. – John Wooden",
        "To live a creative life, we must lose our fear of being wrong. – Anonymous",
        "If you are not willing to risk the usual you will have to settle for the ordinary. – Jim Rohn",
        "Trust because you are willing to accept the risk, not because it’s safe or certain. – Anonymous",
        "All our dreams can come true if we have the courage to pursue them. – Walt Disney",
        "Good things come to people who wait, but better things come to those who go out and get them. – Anonymous",
        "If you do what you always did, you will get what you always got. – Anonymous",
        "Success is walking from failure to failure with no loss of enthusiasm. – Winston Churchill",
        "Just when the caterpillar thought the world was ending, he turned into a butterfly. – Proverb",
        "Successful entrepreneurs are givers and not takers of positive energy. – Anonymous",
        "Whenever you see a successful person you only see the public glories, never the private sacrifices to reach them. – Vaibhav Shah",
        "Opportunities don't happen, you create them. – Chris Grosser",
        "Try not to become a person of success, but rather try to become a person of value. – Albert Einstein",
        "Great minds discuss ideas; average minds discuss events; small minds discuss people. – Eleanor Roosevelt",
        "I find that the harder I work, the more luck I seem to have. – Thomas Jefferson",
        "The starting point of all achievement is desire. – Napoleon Hill",
        "Success is the sum of small efforts, repeated day-in and day-out. – Robert Collier",
        "If you want to lift yourself up, lift up someone else. – Booker T. Washington",
        "Only put off until tomorrow what you are willing to die having left undone. – Pablo Picasso",
        "People rarely succeed unless they have fun in what they are doing. – Dale Carnegie",
        "Motivation is what gets you started. Habit is what keeps you going. – Jim Ryun",
        "The harder you work for something, the greater you’ll feel when you achieve it. – Anonymous",
        "Don’t watch the clock; do what it does. Keep going. – Sam Levenson",
        "Great things never come from comfort zones. – Anonymous",
        "Push yourself, because no one else is going to do it for you. – Anonymous",
        "Sometimes we’re tested not to show our weaknesses, but to discover our strengths. – Anonymous"
    ]

    if "profile_quote" not in st.session_state:
        st.session_state.profile_quote = random.choice(quotes)

    st.info(f"“{st.session_state.profile_quote}”")

    if st.button("Refresh quote", use_container_width=True):
        st.session_state.profile_quote = random.choice(quotes)
        st.rerun()

    st.divider()

    st.markdown("### Current focus")

    st.markdown(
        """
        - Agentic AI workflows
        - Explainable decision support
        - AI governance and evaluation
        - Product strategy and value realization
        - Federated and privacy-preserving AI
        """
    )

    st.divider()

    st.markdown("### Connect")

    st.link_button(
        "GitHub profile",
        "https://github.com/bneelkamal",
        use_container_width=True,
    )

    st.link_button(
        "LinkedIn",
        "https://www.linkedin.com/in/bneelkamal/",
        use_container_width=True,
    )


st.markdown(
    """
<div class="hero">
  <div class="eyebrow">
    AI Portfolio · Product Management · Responsible Innovation · BFSI
  </div>
  <h1>Neelkamal Badana</h1>
  <p>
    <strong>Product Manager with 14 years of experience</strong>
    building business outcomes through technology, now combining product
    leadership with advanced AI research.
  </p>
  <p>
    I design practical, explainable, and responsible AI systems for decision
    support, analytics, risk, and organizational intelligence.
  </p>
</div>
""",
    unsafe_allow_html=True,
)


links = st.columns(4)

links[0].link_button(
    "GitHub",
    "https://github.com/bneelkamal",
    use_container_width=True,
)

links[1].link_button(
    "AI Portfolio",
    "https://github.com/bneelkamal/ai-portfolio",
    use_container_width=True,
)

links[2].link_button(
    "LinkedIn",
    "https://www.linkedin.com/in/bneelkamal/",
    use_container_width=True,
)

links[3].link_button(
    "Contact",
    "https://www.linkedin.com/in/bneelkamal/",
    use_container_width=True,
)


st.header("About")

st.markdown(
    """
I am a Product Manager with 14 years of experience in BFSI with an MBA in Finance & Project Management and a Master's student
in Artificial Intelligence, aspiring to pursue doctoral research at the
intersection of AI and business management. My work connects product strategy,
stakeholder communication, business-value analysis, AI system design, and
responsible deployment.
"""
)


st.header("Research interests")

research_tags = [
    "Federated Learning",
    "Vertical FL",
    "Neuro-symbolic AI",
    "Agentic AI",
    "Multi-agent Systems",
    "Explainable AI",
    "AI Governance",
    "Cloud AI/ML",
    "Fraud Detection",
    "Anomaly Detection",
    "MARL",
    "AI for Business",
]

st.markdown(
    '<div>'
    + "".join(
        f'<span class="tag">{tag}</span>'
        for tag in research_tags
    )
    + "</div>",
    unsafe_allow_html=True,
)


st.header("Experience and strengths")

st.markdown(
    '<p class="section-note">'
    "A product-led approach to building and evaluating intelligent systems."
    "</p>",
    unsafe_allow_html=True,
)

strengths = st.columns(3)

strength_data = [
    (
        "Product leadership",
        "Problem discovery, roadmap definition, stakeholder alignment, "
        "prioritization, and value realization.",
    ),
    (
        "AI systems thinking",
        "Translating research concepts into architectures, prototypes, "
        "workflows, and measurable experiments.",
    ),
    (
        "Responsible delivery",
        "Explainability, governance, security, evaluation, human oversight, "
        "and practical adoption constraints.",
    ),
]

for column, (title, text) in zip(strengths, strength_data):
    column.markdown(
        f"""
        <div class="card">
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.header("Featured AI portfolio projects")

st.markdown(
    '<p class="section-note">'
    "Focused projects showing how AI capabilities become useful, "
    "testable products."
    "</p>",
    unsafe_allow_html=True,
)


projects = [
    (
        "Agentic AI Data Analyst",
        "Upload CSV/XLSX files or paste public URLs. A LangGraph workflow "
        "profiles the source, recommends reports, and presents charts and "
        "evidence-grounded insights.",
        "In development",
        "https://github.com/bneelkamal/ai-portfolio/tree/main/projects/ai-data-analyst",
        "pages/01_Agentic_AI_Data_Analyst.py",
    ),
    (
        "RAG Document Intelligence Assistant",
        "An enterprise-style assistant for grounded document search, "
        "citations, and knowledge workflows.",
        "Planned",
        "https://github.com/bneelkamal/ai-portfolio",
        None,
    ),
    (
        "Explainable Fraud Detection",
        "Risk analytics with imbalance handling, anomaly detection, "
        "threshold decisions, and interpretable explanations.",
        "Planned",
        "https://github.com/bneelkamal/ai-portfolio",
        None,
    ),
    (
        "Agentic Business Research Assistant",
        "A multi-agent workflow for research planning, evidence collection, "
        "synthesis, and review.",
        "Planned",
        "https://github.com/bneelkamal/ai-portfolio",
        None,
    ),
    (
        "Responsible AI Evaluation Toolkit",
        "Practical checks for reliability, traceability, explainability, "
        "selected fairness risks, and governance readiness.",
        "Planned",
        "https://github.com/bneelkamal/ai-portfolio",
        None,
    ),
    (
        "Federated Learning Research",
        "Privacy-preserving collaborative learning and fraud-risk research "
        "maintained in a separate research repository.",
        "Research repository",
        "https://github.com/bneelkamal",
        None,
    ),
]


for start in range(0, len(projects), 3):
    row = st.columns(3)

    for column, project in zip(row, projects[start:start + 3]):
        title, description, status, source, demo = project

        card = f"""
        <div class="card">
            <h3>{title}</h3>
            <p>{description}</p>
            <span class="tag">{status}</span>
        </div>
        """

        column.markdown(card, unsafe_allow_html=True)

        button_cols = column.columns(2)

        if source:
            button_cols[0].link_button(
                "Source",
                source,
                use_container_width=True,
            )

        if demo:
            button_cols[1].page_link(
                demo,
                label="Open app",
                icon="🚀",
                use_container_width=True,
            )
        else:
            button_cols[1].link_button(
                "Portfolio",
                "https://github.com/bneelkamal/ai-portfolio",
                use_container_width=True,
            )


st.header("How I approach AI products")

steps = st.columns(4)

step_data = [
    (
        "01",
        "Frame",
        "Define the user problem, business value, and constraints.",
    ),
    (
        "02",
        "Design",
        "Choose the data, architecture, model, tools, and "
        "human-oversight boundaries.",
    ),
    (
        "03",
        "Evaluate",
        "Measure technical quality, usefulness, trust, safety, "
        "and limitations.",
    ),
    (
        "04",
        "Adopt",
        "Plan rollout, governance, stakeholder enablement, "
        "and continuous improvement.",
    ),
]

for column, (number, title, text) in zip(steps, step_data):
    column.markdown(
        f"""
        <div class="card">
            <div class="eyebrow">{number}</div>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.header("Connect")

st.markdown(
    """
For product leadership, AI research, collaboration, or responsible AI
opportunities, connect with me through GitHub or LinkedIn.
"""
)

st.caption(
    "© Neelkamal Badana · AI Product Management and Research Portfolio"
)
