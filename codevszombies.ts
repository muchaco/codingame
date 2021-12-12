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
    return Math.floor(Math.sqrt((a['x'] - b['x']) ** 2 + a['y'] - b['y']))
}

const calculateAction = function (input: Object): Object {
    let worstZombie = null;
    let worstDistance = null;

    Object.entries(input['zombies']).forEach(function ([zombieId, zombieObject]) {
        let nearestHuman = null;
        let nearestDistance = null;

        Object.entries(input['humans']).forEach(function ([humanId, humanObject]) {
            let distanceCandidate = distance(humanObject, zombieObject)
            if (nearestHuman === null || distanceCandidate < nearestDistance) {
                nearestDistance = distanceCandidate;
                nearestHuman = humanId;
            }
        })

        if (worstZombie === null || nearestHuman < worstDistance) {
            worstDistance = nearestHuman;
            worstZombie = zombieId;
        }
    })

    return {
        'x': input['zombies'][worstZombie]['x'],
        'y': input['zombies'][worstZombie]['y']
    }
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
