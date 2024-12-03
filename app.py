from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample questions and feedback
questions = [
    {
        'id': 1,
        'question': 'How far along are you in your business planning?',
        'options': [
            'Just dreaming about how my business idea could be sooooo good.',
            'Have some ideas about how to make it work but not solidified.',
            'Working on it actively—watch out world!',
            'Nearly ready to launch; let’s do this!'
        ],
        'feedback': [
            'First of all, it’s fantastic that you’re dreaming big! Every business starts with an idea, and now it’s time to take action.',
            'You’re making great progress! Solidify those ideas into a detailed plan.',
            'You’re on the right path! Stay focused and refine your plan.',
            'You’re almost there! Focus on the final details for a successful launch.'
        ]
    },
    {
        'id': 2,
        'question': 'Do you have a name for your business?',
        'options': [
            'Yes!',
            'No 😢'
        ],
        'feedback': [
            'The fact that you’ve already picked a name means you’re quite ahead of the game. Now is the time to make sure it’s available for both your domain and social media accounts.',
            'Choosing a name is a key step in branding. Start brainstorming ideas that resonate with your product and audience!'
        ]
    },

    {
        'id': 3,
        'question': 'How do you feel about taking the leap into entrepreneurship?',
        'options': [
            'Excited! I’m ready to make my mark on the world. The only reason why business isn’t running yet is because I don’t have everything I need to launch.',
            'Nervous, but I’m excited about embracing the challenge.',
            'Overwhelmed. That’s probably the reason I haven’t done anything about it',
            'Scared stiff. Who am I kidding? I will never be able to run my own business'
        ],
        'feedback': [
            'Thinking about why you’re doing this is very important, and it’s really amazing that you’re passionate about what you do! That passion will keep you motivated and help you power through challenges. Focusing on the work you love will make the journey more fulfilling.',
            'Thinking about why you’re doing this is very important, and recognizing a market gap is a great strategy. Just make sure that when you’re marketing, you position yourself as the solution that fills the void in the market!',
            'Thinking about why you’re doing this is very important, and passion paired with market demand gives you the best of both worlds. Keep using your passion to fuel your business while tapping into the market’s needs for lasting success.',
            'Thinking about why you’re doing this is very important, and it’s totally okay to be unsure in the beginning! Take time to explore what excites you about the business. Your "why" will become clearer as you continue to grow and define your vision.'
        ]
    },

    {
        'id': 4,
        'question': 'Do you have the skills or knowledge needed to run this business',
        'options': [
            'Yes, I’m a business whiz! 💪',
            'Somewhat confident but could learn a thing or two.',
            'Need to improve my skills; time to hit the books! 📖',
            'Plan to work with a co-founder or mentor for guidance.'
        ],
        'feedback': [
            'By the way, its great that you’re excited about your business! That’s the fuel that’ll keep it going to the launch. Just make sure you sit down to some planning and then you’ve got no excuses.',
            'By the way, it’s natural to feel a mix of excitement, nervousness, and even overwhelm when starting a business. If you’re excited but still gathering your resources, that’s great—preparation is key to making your launch successful.',
            'By the way, it’s normal to feel overwhelmed at the thought of running a business. The best thing to do to get the ball rolling is to break down your to-do list into smaller steps and take it one day at a time. ',
            'By the way, it’s normal to feel overwhelmed at the thought of running a business. Remember—every entrepreneur has doubts at some point. With the right mindset and support, you can and should absolutely make it happen.'
        ]
    },

    {
        'id': 5,
        'question': 'Do you have the skills or knowledge needed to run this business',
        'options': [
            'Yes, I’m a business whiz! 💪',
            'Somewhat confident but could learn a thing or two.',
            'Need to improve my skills; time to hit the books! 📖',
            'Plan to work with a co-founder or mentor for guidance.'
        ],
        'feedback': [
            'By the way, its great that you’re excited about your business! That’s the fuel that’ll keep it going to the launch. Just make sure you sit down to some planning and then you’ve got no excuses.',
            'By the way, it’s natural to feel a mix of excitement, nervousness, and even overwhelm when starting a business. If you’re excited but still gathering your resources, that’s great—preparation is key to making your launch successful.',
            'By the way, it’s normal to feel overwhelmed at the thought of running a business. The best thing to do to get the ball rolling is to break down your to-do list into smaller steps and take it one day at a time. ',
            'By the way, it’s normal to feel overwhelmed at the thought of running a business. Remember—every entrepreneur has doubts at some point. With the right mindset and support, you can and should absolutely make it happen.'
        ]
    },

    {
    'id': 6,
    'question': 'Do you know others in your industry or field?',
    'options': [
        'Yes, I have a network of awesome people!',
        'I know a few, but I want to expand my circle!',
        'I don’t know anyone in this field—time to change that!',
        'I’m actively building my connections—lets grow together!'
    ],
    'feedback': [
        'Your business is probably going to take up more of your time than you realize, especially at the start. By focusing on high-impact tasks, you can still make progress in the early stages. Prioritize wisely, and every hour will count.',
        'Your business is probably going to take up more of your time than you realize, especially at the start, and with 10-20 hours a week, you’re in a great position to start building momentum. Use this time to work on key areas like marketing, planning, and operations that will move your business forward.',
        'Your business is probably going to take up more of your time than you realize, especially at the start, and you’ve committed to making your business a priority, which is fantastic! With this 20-40 hours a week, you can develop strong systems and processes and make rapid progress on your goals.',
        'Your business is probably going to take up more of your time than you realize, especially at the start, and it’s incredible that you’re fully dedicated to moving at full speed. Use this time to execute your plans, test new ideas, and build a strong foundation for your business.'
    ]
},
{
    'id': 7,
    'question': 'Why are you starting this business? Is it because you enjoy the work involved, or because you see a great opportunity for success in the market?',
    'options': [
        'I love the work! (e.g., I enjoy baking cakes)',
        'I see a market gap! (e.g., My area lacks good bakeries, so I see a big opportunity.)',
        'Both! (e.g., I love baking, and I know there’s demand for it.)',
        'I’m not sure yet. (e.g., I just want to start something and baking sounds like a good idea.)'
    ],
    'feedback': [
        'Just a little note: Never underestimate the power of a solid network. Keep nurturing your business-related relationships, as they’ll provide support, advice, and opportunities that will help your business grow.',
        'Just a little note: Never underestimate the power of a solid network. Expanding your circle is essential for growth. Continue reaching out to others in your field, attend events, and engage online to broaden your connections and open up new opportunities.',
        'Just a little note: Never underestimate the power of a solid network —and it’s never too late to start making business relationships! Start by reaching out to others in your field. You don’t have to talk to direct competition, but people who can help you understand your audience and will be able to vouch for you in the future. The relationships you build now will help you as your business grows.',
        'Just a little note: Never underestimate the power of a solid network. Start by reaching out to others in your field. You don’t have to talk to direct competition, but people who can help you understand your audience and will be able to vouch for you in the future. The relationships you build now will help you as your business grows.'
    ]
},
{
    'id': 8,
    'question': 'How many competitors can you name in three seconds?',
    'options': [
        'One... two... uh... I can’t think of any!',
        'I can name a few—let’s get competitive!',
        'I know my competitors like the back of my hand!',
        'I dont have any competitors—Im one of a kind!'
    ],
    'feedback': [
        'And, it’s totally okay if you’re not sure about competitors yet! Now is the time to research who else is in the market. Understanding your competition will help you position your business more effectively and discover ways to stand out.',
        'And, now that you’ve identified some competitors, take the time to dive deeper into what they’re doing well. Look for gaps or areas where you can offer something different, and continue refining your unique selling points.',
        'And, knowing your competitors is a huge advantage! It keeps you ahead of them. Use this knowledge to sharpen your own strategy, and focus on offering even more value to your customers to keep them engaged.',
        'And, being unique is a strong position to be in, but remember, there may still be indirect competitors. Stay aware of the broader market trends and continue looking for ways to differentiate yourself even further to stay competitive.'
    ]
},
{
    'id': 9,
    'question': 'What’s your “superpower” when it comes to business?',
    'options': [
        '"I’m a visionary—I see possibilities before others do!"',
        '"I’m a problem-solver—I love making things work!"',
        '"I’m a people person—I connect with anyone and everyone!"',
        '"I’m a doer—I get things done, no excuses!"'
    ],
    'feedback': [
        'So, dear visionary. Being able to spot opportunities before others can help you stay ahead of trends and lead your business toward innovative solutions. Trust your instincts and focus on shaping the future of your industry.',
        'So, dear problem-solver. No matter the challenges that arise, you can rely on your ability to find solutions and keep things moving smoothly in your business.',
        'So, dear people-person. Use your ability to build relationships to network, collaborate, and grow your customer base. It will help you connect with others and build lasting partnerships.',
        'So, dear doer. Your ability to take action is exactly what will drive your business forward. Keep that momentum going—focus on getting things done, and watch your business move ahead quickly.'
    ]
},
{
    'id': 10,
    'question': 'How would you imagine your dream business’s vibe?',
    'options': [
        'Fun and playful—let’s make it a party! 🎉',
        'Professional and polished—class all the way.',
        'Bold and innovative—let’s shake things up!',
        'Laid-back and chill—let’s take it easy and steady.'
    ],
    'feedback': [
        '"Youre almost there!"',
        '"Youre almost there!',
        '"Youre almost there!"',
        ' "Youre almost there!"'
    ]
}

]



@app.route('/')
def start_quiz():
    session['responses'] = []
    return redirect(url_for('quiz', question_id=1))


@app.route('/quiz/<int:question_id>', methods=['GET', 'POST'])
def quiz(question_id):
    if request.method == 'POST':
        # Save the response
        selected_option = request.form.get('answer')
        session['responses'].append({'question_id': question_id, 'answer': selected_option})
        session.modified = True

        # Redirect to feedback
        return redirect(url_for('feedback', question_id=question_id))

    # Render the current question
    question = questions[question_id - 1]
    return render_template('quiz.html', question=question, question_id=question_id)

@app.route('/feedback/<int:question_id>')
def feedback(question_id):
    responses = session.get('responses', [])
    current_response = responses[-1]
    question = questions[current_response['question_id'] - 1]
    selected_option = int(current_response['answer'])
    feedback = question['feedback'][selected_option]

    # Check if it's the last question
    is_last_question = question_id == len(questions)

    return render_template('feedback.html', feedback=feedback, question_id=question_id, is_last_question=is_last_question)


@app.route('/summary')
def summary():
    responses = session.get('responses', [])
    summary_feedback = []
    for response in responses:
        question = questions[response['question_id'] - 1]
        selected_option = int(response['answer'])
        summary_feedback.append(question['feedback'][selected_option])

    return render_template('summary.html', summary_feedback=summary_feedback)

if __name__ == '__main__':
    app.run(debug=True)
