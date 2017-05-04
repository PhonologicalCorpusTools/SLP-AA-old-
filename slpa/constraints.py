import sys
import inspect

class DistalMedialCorrespondanceConstraint():
    """
    Medial and distal joints must match in flexion.
    Slots to compare are 18/19,23/24,28/29,33/34
    """
    name = 'Distal Medial Constraint'
    explanation = 'Medial and distal joints must match in flexion'
    constraint_type = 'simple'
    def __init__(self):
        pass

    @classmethod
    def check(cls, transcription):
        output = list()
        if transcription[17] != transcription[18]:
            output.append('18, 19')
        if transcription[22] != transcription[23]:
            output.append('23, 24')
        if transcription[27] != transcription[28]:
            output.append('28, 29')
        if transcription[32] != transcription[33]:
            output.append('33, 34')

        output = ', '.join(output)
        return output

class MedialJointConstraint():
    """
    Medial joints cannot be marked 'H' (hyper-extended).
    Medial joints occupy slots 18, 23, 28, 33
    """
    name = 'Medial Joint Constraint'
    explanation = 'Medial joints cannot be marked \'H\''
    constraint_type = 'simple'

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
    constraint_type = 'transcription'

    def __init__(self):
        pass

    @classmethod
    def check(cls, transcription):
        output = list()
        for slot in transcription[1:]:
            if not slot.text():
                if slot.num in [12, 13, 14, 15]:
                    pass
                else:
                    output.append(str(slot.num))
        return ', '.join(output)


class IndexRingPinkySelectionConstraint():
    """
    Slots 17 and 27 can't be E, H, or i while slots 22 and 32 are F
    """
    name = 'Index-Ring-Pinky Selection Constraint'
    explanation = 'If the middle and pinky proximal joints are flexed, the index and ring proximal joints cannot be extended'
    constraint_type = 'conditional'
    def __init__(self):
        pass

    @classmethod
    def check(cls, transcription):
        output = list()
        if transcription[21].text() == 'F' or transcription[31].text() == 'F':
            if transcription[16].text() in 'EHi':
                output.append('17')
            if transcription[26].text() in 'EHi':
                output.append('27')
        return ', '.join(output)

class IndexMiddlePinkySelectionConstraint():
    """
    Slots 17, 22, and 32 can't be E, H, or i while 27 is F
    """
    name = 'Index-Middle-Pinky Selection Constraint'
    explanation = 'If the ring proximal joint is flexed, the index, middle, and pinky proximal joints cannot be extended'
    constraint_type = 'conditional'
    def __init__(self):
        pass

    @classmethod
    def check(cls, transcription):
        output = list()
        if transcription[26].text() == 'F':
            if transcription[16].text() in 'EHi':
                output.append('17')
            if transcription[21].text() in 'EHi':
                output.append('22')
            if transcription[31].text() in 'EHi':
                output.append('32')
        return ', '.join(output)

class RingPinkyAnatomicalContstraint():
    """
    Slots 33 and 34 can't be F and F while slots 28 and slot 29 are E, H, or i (unless slot 15 is a 4)
    """
    name = 'Ring-Pinky Constraint'
    explanation = ('If the ring medial and distal joints are extended, '
                    'the pinky medial and distal joints cannot be flexed (unless thumb is in contact with pinky)')
    constraint_type = 'conditional'

    def __init__(self):
        pass

    @classmethod
    def check(cls, transcription):
        output = list()
        if transcription[27].text() in 'EHi':
            output.append('27')
        if transcription[28].text() in 'EHi':
            output.append('28')
        if output == ['27', '28']:
            if transcription[14].text() != '4':
                if transcription[32].text() == 'F':
                    output.append('32')
                if transcription[33].text() == 'F':
                    output.append('33')
                output.sort()
                return ', '.join(output)
        else:
            return []

class MajorFeaturesConstraint():
    """
    Major features must be selected
    """
    name = 'Major Features Constraint'
    explanation = ('A transcription must indicate location, movement, and orientation')
    constraint_type = 'transcription'

    def __init__(self):
        pass

    @classmethod
    def check(cls, featuresLayout):
        output = list()
        if not featuresLayout.major.currentText():
            output.append('Major location')
        if not featuresLayout.minor.currentText():
            output.append('Minor location')
        if not featuresLayout.oneHandMovement.currentText():
            output.append('One hand movement')
        if not featuresLayout.twoHandMovement.currentText():
            output.append('Two hand movement')
        if not featuresLayout.orientation.currentText():
            output.append('Orientation')
        if not featuresLayout.dislocation.currentText():
            output.append('Dislocation')
        return output

class SecondHandMovementConstraint():
    name = 'Second Hand Movement Constraint'
    explanation = ('If a sign uses two hands, the second hand must have a movement feature')
    constraint_type = 'transcription'

    def __init__(self):
        pass

    @classmethod
    def check(cls, transcription):
        output = list()
        return output

def sortMasterList(listItem):
    if listItem[1].name == 'No Empty Slots Constraint':
        return 0
    elif listItem[1].constraint_type == 'transcription':
        return 1
    elif listItem[1].constraint_type == 'simple':
        return 2
    elif listItem[1].constraint_type == 'conditional':
        return 3
    else:
        return 4


MasterConstraintList = inspect.getmembers(sys.modules[__name__], inspect.isclass)
MasterConstraintList.sort(key=lambda x:x[1].name)
MasterConstraintList.sort(key=sortMasterList)



