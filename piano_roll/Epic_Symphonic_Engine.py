import flpianoroll
import math
import random

def createDialog():
    """
    Creates the elite orchestration controller panel inside the Piano Roll grid view.
    """
    form = flpianoroll.ScriptDialog("EPIC-STUDIO'S // Symphonic Orchestration Engine", "Applies emotional curves and humanized micro-timings to selected layers.")
    form.addInputKnob("Crescendo Depth", 80, 10, 100)
    form.addInputKnob("Human Micro-Timing", 10, 0, 30)
    form.addInputCombo("Symphonic Mode", "Exponential Crescendo,Linear Swell,Decrescendo", 0)
    return form

def apply(form):
    """
    Executes advanced velocity mapping and subtle micro-timing offsets on human musicianship.
    """
    crescendo_depth = form.getInputValue("Crescendo Depth") / 100.0
    timing_variance = form.getInputValue("Human Micro-Timing")
    selected_mode = form.getInputValue("Symphonic Mode")
    
    score = flpianoroll.score
    if not score.noteCount:
        return

    # Sort the highlighted notes in order of time execution
    notes = [score.getNote(i) for i in range(score.noteCount)]
    notes.sort(key=lambda x: x.time)
    
    start_time = notes[0].time
    end_time = notes[-1].time
    total_duration = end_time - start_time if end_time > start_time else 1

    for note in notes:
        # Calculate relative position within the pattern phrase (0.0 to 1.0)
        progress = (note.time - start_time) / total_duration
        
        # 1. Apply Music Industry Dynamics Curves
        if selected_mode == 0:    # Exponential Crescendo (Ideal for epic cinematic builds)
            velocity_multiplier = math.pow(progress, 2) * crescendo_depth
        elif selected_mode == 1:  # Linear Swell
            velocity_multiplier = progress * crescendo_depth
        else:                     # Decrescendo
            velocity_multiplier = (1.0 - progress) * crescendo_depth
            
        # Blend target velocity with a margin of individual musician variance
        note.velocity = max(0.15, min(1.0, velocity_multiplier + random.uniform(-0.07, 0.07)))
        
        # 2. Apply Micro-Timing Imperfections (Breathes acoustic space into the mix)
        human_jitter = random.randint(-int(timing_variance), int(timing_variance))
        note.time = max(0, note.time + human_jitter)
