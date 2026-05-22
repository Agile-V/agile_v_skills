#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const skills = [
  { name: 'agile-v-core', path: '../agile-v-core/SKILL.md', type: 'core', target: 150 },
  { name: 'agile-v-compliance', path: '../agile-v-compliance/SKILL.md', type: 'governance', target: 300 },
  { name: 'agile-v-pipeline', path: '../agile-v-pipeline/SKILL.md', type: 'governance', target: 300 },
  { name: 'agile-v-lifecycle', path: '../agile-v-lifecycle/SKILL.md', type: 'governance', target: 300 },
  { name: 'agile-v-product-owner', path: '../agile-v-product-owner/SKILL.md', type: 'governance', target: 300 },
  { name: 'build-agent', path: '../build-agent/SKILL.md', type: 'base', target: 300 },
  { name: 'build-agent-nestjs', path: '../domains/build-agent-nestjs/SKILL.md', type: 'domain', target: 500 },
  { name: 'build-agent-js', path: '../domains/build-agent-js/SKILL.md', type: 'domain', target: 500 },
  { name: 'build-agent-python', path: '../domains/build-agent-python/SKILL.md', type: 'domain', target: 500 },
  { name: 'build-agent-dart', path: '../domains/build-agent-dart/SKILL.md', type: 'domain', target: 500 },
  { name: 'build-agent-embedded', path: '../domains/build-agent-embedded/SKILL.md', type: 'domain', target: 500 },
  { name: 'requirement-architect', path: '../requirement-architect/SKILL.md', type: 'specialist', target: 300 },
  { name: 'test-designer', path: '../test-designer/SKILL.md', type: 'specialist', target: 300 },
  { name: 'logic-gatekeeper', path: '../logic-gatekeeper/SKILL.md', type: 'specialist', target: 300 },
  { name: 'red-team-verifier', path: '../red-team-verifier/SKILL.md', type: 'specialist', target: 300 },
  { name: 'compliance-auditor', path: '../compliance-auditor/SKILL.md', type: 'specialist', target: 300 },
  { name: 'release-manager', path: '../release-manager/SKILL.md', type: 'specialist', target: 300 },
  { name: 'threat-modeler', path: '../threat-modeler/SKILL.md', type: 'specialist', target: 300 },
  { name: 'observability-planner', path: '../observability-planner/SKILL.md', type: 'specialist', target: 300 },
  { name: 'ux-spec-author', path: '../ux-spec-author/SKILL.md', type: 'specialist', target: 300 },
  { name: 'documentation-agent', path: '../documentation-agent/SKILL.md', type: 'specialist', target: 300 },
  { name: 'discovery-analyst', path: '../discovery-analyst/SKILL.md', type: 'specialist', target: 300 },
  { name: 'schematic-generator', path: '../schematic-generator/SKILL.md', type: 'specialist', target: 300 },
];

console.log('📊 Agile V Skills Analysis\n');
console.log('═'.repeat(120));

const results = [];
let totalLines = 0;
let totalSize = 0;

skills.forEach(skill => {
  const fullPath = path.join(__dirname, skill.path);
  
  if (!fs.existsSync(fullPath)) {
    console.log(`⚠️  ${skill.name.padEnd(30)} - FILE NOT FOUND`);
    return;
  }

  const content = fs.readFileSync(fullPath, 'utf-8');
  const lines = content.split('\n').length;
  const size = Buffer.byteLength(content, 'utf-8');
  const sizeKB = (size / 1024).toFixed(1);
  
  // Check for sections_index
  const hasSectionsIndex = content.includes('sections_index:');
  
  // Check for metadata
  const hasMetadata = content.match(/^---\n[\s\S]*?\n---/);
  
  // Check for SCOPE-V participation
  const hasScopeV = content.includes('## SCOPE-V Participation') || content.includes('## SCOPE-V');
  
  // Check for inheritance
  const extendsMatch = content.match(/extends:\s*['"]?([^'"}\n]+)/);
  const extendsSkill = extendsMatch ? extendsMatch[1].trim() : null;
  
  // Check for evidence requirements
  const hasEvidence = content.includes('## Evidence Requirements');
  
  // Target comparison
  const percentOfTarget = ((lines / skill.target) * 100).toFixed(0);
  const status = lines <= skill.target ? '✅' : '⚠️';
  
  results.push({
    name: skill.name,
    type: skill.type,
    lines,
    size,
    sizeKB,
    target: skill.target,
    percentOfTarget,
    status,
    hasSectionsIndex,
    hasMetadata,
    hasScopeV,
    extendsSkill,
    hasEvidence
  });
  
  totalLines += lines;
  totalSize += size;
});

// Sort by type and then by name
results.sort((a, b) => {
  if (a.type !== b.type) {
    const typeOrder = { core: 1, governance: 2, base: 3, domain: 4, specialist: 5 };
    return typeOrder[a.type] - typeOrder[b.type];
  }
  return a.name.localeCompare(b.name);
});

// Display by category
let currentType = null;
results.forEach(r => {
  if (r.type !== currentType) {
    currentType = r.type;
    console.log('\n' + r.type.toUpperCase().padEnd(120, ' '));
    console.log('─'.repeat(120));
  }
  
  const nameCol = r.name.padEnd(30);
  const linesCol = `${r.lines}`.padStart(5);
  const targetCol = `${r.target}`.padStart(5);
  const percentCol = `${r.percentOfTarget}%`.padStart(5);
  const sizeCol = `${r.sizeKB}KB`.padStart(8);
  
  const features = [];
  if (r.hasSectionsIndex) features.push('idx');
  if (r.hasScopeV) features.push('scope');
  if (r.extendsSkill) features.push(`ext:${r.extendsSkill}`);
  if (r.hasEvidence) features.push('evid');
  const featuresCol = features.join(' | ').padEnd(35);
  
  console.log(`${r.status} ${nameCol} ${linesCol}/${targetCol} (${percentCol}) ${sizeCol}  ${featuresCol}`);
});

console.log('\n' + '═'.repeat(120));
console.log('\n📈 Summary Statistics\n');

const byType = results.reduce((acc, r) => {
  if (!acc[r.type]) acc[r.type] = { count: 0, lines: 0, size: 0 };
  acc[r.type].count++;
  acc[r.type].lines += r.lines;
  acc[r.type].size += r.size;
  return acc;
}, {});

Object.entries(byType).forEach(([type, stats]) => {
  const avgLines = Math.round(stats.lines / stats.count);
  const avgSizeKB = (stats.size / stats.count / 1024).toFixed(1);
  console.log(`${type.padEnd(15)} ${stats.count} skills  │  Avg: ${avgLines} lines, ${avgSizeKB}KB  │  Total: ${stats.lines} lines`);
});

console.log('\n' + '─'.repeat(120));
console.log(`Total: ${results.length} skills  │  ${totalLines} lines  │  ${(totalSize / 1024).toFixed(1)}KB`);

// Modernization recommendations
console.log('\n\n🔧 Modernization Recommendations\n');
console.log('═'.repeat(120));

const needsSectionsIndex = results.filter(r => !r.hasSectionsIndex && r.type !== 'core');
if (needsSectionsIndex.length > 0) {
  console.log(`\n📋 Add sections_index (${needsSectionsIndex.length} skills):`);
  needsSectionsIndex.forEach(r => console.log(`   - ${r.name}`));
}

const domainWithoutScopeV = results.filter(r => r.type === 'domain' && !r.hasScopeV);
if (domainWithoutScopeV.length > 0) {
  console.log(`\n🎯 Add SCOPE-V participation (${domainWithoutScopeV.length} domain skills):`);
  domainWithoutScopeV.forEach(r => console.log(`   - ${r.name}`));
}

const domainWithoutInheritance = results.filter(r => r.type === 'domain' && !r.extendsSkill);
if (domainWithoutInheritance.length > 0) {
  console.log(`\n🔗 Add inheritance metadata (${domainWithoutInheritance.length} domain skills):`);
  domainWithoutInheritance.forEach(r => console.log(`   - ${r.name}`));
}

const overTarget = results.filter(r => r.lines > r.target);
if (overTarget.length > 0) {
  console.log(`\n⚠️  Skills exceeding target (${overTarget.length} skills):`);
  overTarget.forEach(r => {
    const excess = r.lines - r.target;
    console.log(`   - ${r.name.padEnd(30)} ${r.lines}/${r.target} (+${excess} lines, ${r.percentOfTarget}%)`);
  });
}

// Context efficiency analysis
console.log('\n\n💡 Context Usage Analysis\n');
console.log('═'.repeat(120));

// Typical workflows
const workflows = [
  {
    name: 'NestJS Feature (Modern)',
    skills: ['agile-v-core', 'build-agent', 'build-agent-nestjs'],
    baseline: 200000
  },
  {
    name: 'Python Feature',
    skills: ['agile-v-core', 'build-agent', 'build-agent-python'],
    baseline: 200000
  },
  {
    name: 'Full Compliance Workflow',
    skills: ['agile-v-core', 'agile-v-compliance', 'requirement-architect', 'build-agent', 
             'build-agent-nestjs', 'test-designer', 'red-team-verifier', 'compliance-auditor'],
    baseline: 200000
  },
  {
    name: 'Release Pipeline',
    skills: ['agile-v-pipeline', 'release-manager', 'compliance-auditor'],
    baseline: 200000
  }
];

workflows.forEach(workflow => {
  const skillsData = workflow.skills.map(name => results.find(r => r.name === name)).filter(Boolean);
  const totalContext = skillsData.reduce((sum, s) => sum + s.size, 0);
  const totalContextKB = (totalContext / 1024).toFixed(1);
  const percentOfBaseline = ((totalContext / workflow.baseline) * 100).toFixed(1);
  
  const status = totalContext < workflow.baseline * 0.5 ? '✅' : 
                 totalContext < workflow.baseline * 0.7 ? '⚠️' : '❌';
  
  console.log(`${status} ${workflow.name.padEnd(35)} ${totalContextKB}KB  (${percentOfBaseline}% of ${workflow.baseline / 1000}K context)`);
  console.log(`   Skills: ${workflow.skills.join(', ')}`);
});

console.log('\n' + '═'.repeat(120));
console.log('\n✅ Analysis complete!\n');
