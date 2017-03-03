class DistalMedialCorrespondanceConstraint():
    """
    Medial and distal joints must match in flexion.
    Slots to compare are 18/19,23/24,28/29,33/34
    """
    name = 'Distal Medial Constraint'
    explanation = 'Medial and distal joints must match in flexion'
    def __init__(self):
        pass

    @classmethod
    def check(cls, transcription):
        output = list()
        if transcription[17] != transcription[18]:
            output.append('18/19')
        if transcription[22] != transcription[23]:
            output.append('23/24')
        if transcription[27] != transcription[28]:
            output.append('28/29')
        if transcription[32] != transcription[33]:
            output.append('33/34')

        output = ', '.join(output)
        return output

class MedialJointConstraint():
    """
    Medial joints cannot be marked 'H' (hyper-extended).
    Medial joints occupy slots 18, 23, 28, 33
    """
    name = 'Medial Joint Constraint'
    explanation = 'Medial joints cannot be marked \'H\''

    def __init__(self):
        pass

    @classmethod
    def check(cls, transcription):
        output = list()
        if transcription[17].text() == 'H':
            output.append('18')
        if transcription[22].text() == 'H':
            output.append('23')
        if transcription[27].text() == 'H':
            output.append('28')
        if transcription[32].text() == 'H':
            output.append('33')
        if output:
            output = ', '.join(output)
        return output

class NoEmptySlotsConstraint():
    """
    Every transcription slot must be filled. For Field 3, where emtpy slots are possible, this constraint
    demands that some symbol be used to represent empty slots (the default option is to use dashes)
    """
    name = 'No Empty Slots Constraint'
    explanation = 'Every transcription slot must have a value'

    def __init__(self):
        pass

    @classmethod
    def check(cls, transcription):
        output = list()
        for slot in transcription[1:]:
            if not slot.text():
                output.append(str(slot.num))
        return ','.join(output)