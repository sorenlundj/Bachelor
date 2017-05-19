import gc
import os
import nose
import pickle
import logging

import angr

l = logging.getLogger("angr.tests")
test_location = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../binaries/tests'))

target_addrs = {
    'i386': [ 0x080485C9 ],
    'x86_64': [ 0x4006ed ],
    'ppc': [ 0x1000060C ],
    'armel': [ 0x85F0 ],
    'android/arm': [ 0x4004cc ],
    'mips': [ 0x4009FC ]
}

avoid_addrs = {
    'i386': [ 0x080485DD,0x08048564 ],
    'x86_64': [ 0x4006aa,0x4006fd ],
    'ppc': [ 0x10000644,0x1000059C ],
    'armel': [ 0x86F8,0x857C ],
    'android/arm': [ 0x4004f0,0x400470 ],
    'mips': [ 0x400A10,0x400774 ]
}

corrupt_addrs = {
    'i386': [ 0x80486B6, 'bO\xcc', lambda s: s.memory.store(s.regs.esp, s.regs.eax) ],
    'x86_64': [ 0x400742, '\xd4&\xb0[\x41', lambda s: s.registers.store('rdx', 8) ],
    'ppc': [ 0x100006B8, '\x05\xad\xc2\xea', lambda s: s.registers.store('r5', 8) ],
    'armel': [ 0x8678, '\xbdM\xec3', lambda s: s.registers.store('r2', 8) ],
    'mips': [ 0x400918, '[\xf8\x96@'[::-1], lambda s: s.registers.store('a2', 8) ]
}

divergences = {
    'ppc': 0x10000588,
    'x86_64': 0x40068e,
    'i386': 0x8048559,
    'armel': 0x8568,
    'android/arm': 0x40045c,
    'mips': 0x40075c,
}

def run_fauxware(arch):
    p = angr.Project(os.path.join(test_location, arch, "fauxware"))
    results = p.factory.path_group().explore(find=target_addrs[arch], avoid=avoid_addrs[arch])
    stdin = results.found[0].state.posix.dumps(0)
    nose.tools.assert_equal('\x00\x00\x00\x00\x00\x00\x00\x00\x00SOSNEAKY\x00', stdin)

    # test the divergence detection
    ancestor = results.found[0].history.closest_common_ancestor((results.avoid + results.active)[0].history)
    divergent_point = list(angr.path.HistoryIter(results.found[0].history, end=ancestor))[0]
    #p.factory.block(divergent_point.addr).pp()
    assert divergent_point.addr == divergences[arch]

def run_pickling(arch):
    p = angr.Project(os.path.join(test_location, arch, "fauxware"))
    pg = p.factory.path_group().step(n=10)
    pickled = pickle.dumps(pg, pickle.HIGHEST_PROTOCOL)
    del p
    del pg
    gc.collect()
    pg = pickle.loads(pickled)

    pg.explore(find=target_addrs[arch], avoid=avoid_addrs[arch])
    stdin = pg.found[0].state.posix.dumps(0)
    nose.tools.assert_equal('\x00\x00\x00\x00\x00\x00\x00\x00\x00SOSNEAKY\x00', stdin)

def run_fastmem(arch):
    p = angr.Project(os.path.join(test_location, arch, "fauxware"))
    p.analyses.CongruencyCheck(throw=True).set_state_options(right_add_options={"FAST_REGISTERS"}).run()

def run_nodecode(arch):
    p = angr.Project(os.path.join(test_location, arch, "fauxware"))

    # screw up the instructions and make sure the test fails with nodecode
    for i,c in enumerate(corrupt_addrs[arch][1]):
        p.loader.memory[corrupt_addrs[arch][0] + i] = c
    boned = p.factory.path_group().explore(find=target_addrs[arch], avoid=avoid_addrs[arch])
    nose.tools.assert_true(len(boned.errored) >= 1)
    nose.tools.assert_true(isinstance(boned.errored[0].error, angr.AngrExitError))
    nose.tools.assert_true(boned.errored[0].addr == corrupt_addrs[arch][0])

    # hook the instructions with the emulated stuff
    p.hook(corrupt_addrs[arch][0], corrupt_addrs[arch][2], length=len(corrupt_addrs[arch][1]))
    results = p.factory.path_group().explore(find=target_addrs[arch], avoid=avoid_addrs[arch])
    stdin = results.found[0].state.posix.dumps(0)
    nose.tools.assert_equal('\x00\x00\x00\x00\x00\x00\x00\x00\x00SOSNEAKY\x00', stdin)

def run_merge(arch):
    p = angr.Project(os.path.join(test_location, arch, "fauxware"))
    pg = p.factory.path_group()
    pg.explore()
    pg.merge(stash='deadended')

    path = pg.deadended[[ 'Welcome' in s for s in pg.mp_deadended.state.posix.dumps(1).mp_items ].index(True)]
    yes, no = sorted(path.history.merge_conditions, key=lambda c: c.depth)
    inp = path.state.posix.files[0].content.load(0, 18)
    assert 'SOSNEAKY' in path.state.se.any_str(inp, extra_constraints=(yes,))
    assert 'SOSNEAKY' not in path.state.se.any_str(inp, extra_constraints=(no,))

def test_merge():
    for arch in target_addrs:
        yield run_merge, arch

def test_fauxware():
    for arch in target_addrs:
        yield run_fauxware, arch

def test_pickling():
    for arch in corrupt_addrs:
        yield run_pickling, arch

def test_fastmem():
    #for arch in target_addrs:
    #   yield run_fastmem, arch
    # TODO: add support for comparing flags of other architectures
    #yield run_fastmem, "i386"
    yield run_fastmem, "x86_64"
    #yield run_fastmem, "ppc"
    #yield run_fastmem, "mips"

def test_nodecode():
    for arch in corrupt_addrs:
        yield run_nodecode, arch

if __name__ == "__main__":
    for r,a in test_merge():
        r(a)
    for r,a in test_fauxware():
        r(a)
    for r,a in test_pickling():
        r(a)