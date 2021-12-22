const height = 9000;
const width = 16000;
const move = 1000;
const zombieMove = 400;


const parseInput = function () {
    const inputs = {
        'ash': { 'x': null, 'y': null },
        'humans': {},
        'zombies': {}
    };

    const ash: string[] = readline().split(' ');
    inputs.ash.x = parseInt(ash[0]);
    inputs.ash.y = parseInt(ash[1]);

    const aliveHumans = parseInt(readline());
    for (let i = 0; i < aliveHumans; i++) {
        const human: string[] = readline().split(' ');
        const humanId: number = parseInt(human[0]);
        const humanX: number = parseInt(human[1]);
        const humanY: number = parseInt(human[2]);
        inputs.humans[humanId] = { 'x': humanX, 'y': humanY };
    }

    const zombieCount: number = parseInt(readline());
    for (let i = 0; i < zombieCount; i++) {
        const zombie: string[] = readline().split(' ');
        const zombieId: number = parseInt(zombie[0]);
        const zombieX: number = parseInt(zombie[1]);
        const zombieY: number = parseInt(zombie[2]);
        const zombieXNext: number = parseInt(zombie[3]);
        const zombieYNext: number = parseInt(zombie[4]);
        inputs.zombies[zombieId] = {
            'x': zombieX,
            'y': zombieY,
            'nextX': zombieXNext,
            'nextY': zombieYNext
        };
    }

    return inputs;
}


const distance = function (a: Object, b: Object) {
    return Math.floor(Math.sqrt((a['x'] - b['x']) ** 2 + (a['y'] - b['y']) ** 2))
}


const inLine = function (a: Object, b: Object, c: Object) {
    const d1 = distance(a, b);
    const d2 = distance(b, c);
    const d3 = distance(a, c);
    let sorted = [d1, d2, d3];
    sorted.sort(function (a, b) { return a - b });
    console.error(`${sorted}`)
    if (sorted[0] + sorted[1] - sorted[2] < 3) {
        console.error('egyvonelbenvannak');
        return true;
    } else {
        console.error('nincsnewkje gyvonalban');
        return false;
    }
}


const canBeSaved = function (ash: Object, human: Object, zombie: Object) {
    let ourDistance = distance(ash, human);
    let theirDistance = distance(human, zombie);
    let myTurn = ourDistance / move;
    let theirTurn = theirDistance / zombieMove;
    if (theirTurn > myTurn) {
        console.error('megmentheto');
        return true;
    } else {

        console.error('nemmegmentheto');
        return false;
    }
}


const calculateAction = function (input: Object): Object {
    let worstHuman = null;
    let worstDistance = null;

    Object.entries(input['humans']).forEach(function ([humanId, humanObject]) {
        Object.entries(input['zombies']).forEach(function ([_, zombieObject]) {
            let nextZombie = {
                'x': zombieObject['nextX'],
                'y': zombieObject['nextY']
            }

            if (!(inLine(humanObject, zombieObject, nextZombie))) {
                return;
            }

            let distanceCandidate = distance(humanObject, zombieObject)

            if (worstHuman === null || distanceCandidate < worstDistance) {
                if (canBeSaved(input['ash'], humanObject, zombieObject)) {
                    worstDistance = distanceCandidate;
                    worstHuman = humanId;
                }
            } else {
            }
        })
    })

    if (worstHuman === null) {
        return input['ash'];
    }
    return input['humans'][worstHuman];
}


const generateOutput = function (action: Object): void {
    console.log(`${action['x']} ${action['y']}`);
}


while (true) {
    try {
        let inputs = parseInput();
        let action = calculateAction(inputs);
        generateOutput(action);
    } catch (e) {
        console.error(e);
    }
}
