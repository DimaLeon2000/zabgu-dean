// аннотация
$(document).ready(function() {
    $('select[name=spec-input]').select2();
    $('select[name=group-input]').select2();
    $('select[name=stud-input]').select2();
    $('select[name=sort-input]').select2();
    updateTable('', '', '', $('input[name=score-zeroes-input]').prop('checked'), $('select[name=sort-input]').val());
});

// поиск группы по специальности
$(async function () {
    var options = {
            era: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            weekday: 'long',
            timezone: 'UTC',
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric'
        }
    // этап №1.
    $('select[name=spec-input]').change(async function () {
        const id = $(this).val();
        // $('select[name=group-input]').prop("disabled", true);
        // $('select[name=stud-input]').prop("disabled", true);
        $('select[name=group-input]').empty();
        $('select[name=stud-input]').empty();
        $('select[name=group-input]').append(`<option value>-</option>`)
        $('select[name=stud-input]').append(`<option value>-</option>`)
        if (id) {
            await $.get(`api/get_groups/${id}`, function (data) {
                data.result.forEach((item) => {
                    $('select[name=group-input]').append(`<option value="${item.id}">${item.name}</option>`);
                });
            });
            await $.get(`api/get_students_spec/${id}`, function (data) {
                data.result.forEach((item) => {
                    $('select[name=stud-input]').append(`<option value="${item.id}">${item.surname} ${item.firstname.substring(0,1)}.${item.lastname.substring(0,1)}.</option>`);
                });
            });
            // $('select[name=group-input]').prop("disabled", false);
        } else {
            await $.get(`api/groups/`, function (data) {
                data.forEach((item) => {
                    $('select[name=group-input]').append(`<option value="${item.id}">${item.name}</option>`);
                });
            });
            await $.get(`api/students/`, function (data) {
                data.forEach((item) => {
                    $('select[name=stud-input]').append(`<option value="${item.id}">${item.surname} ${item.firstname.substring(0,1)}.${item.lastname.substring(0,1)}.</option>`);
                });
            });
        }
        updateTable(id, '', '', $('input[name=score-zeroes-input]').prop('checked'), $('select[name=sort-input]').val());
    });
    // этап №2.
    $('select[name=group-input]').change(async function () {
        const groupId = $(this).val();
        const specId = $('select[name=spec-input]').val();
        // $('select[name=stud-input]').prop("disabled", true);
        $('select[name=stud-input]').empty();
        $('select[name=stud-input]').append(`<option value>-</option>`)
        if (groupId) {
            await $.get(`api/get_students_group/${groupId}`, function (data) {
                data.result.forEach((item) => {
                    $('select[name=stud-input]').append(`<option value="${item.id}">${item.firstname} ${item.lastname} ${item.surname}</option>`);
                });
            });
            // $('select[name=stud-input]').prop("disabled", false);
        } else if (specId) {
            await $.get(`api/get_students_spec/${specId}`, function (data) {
                data.result.forEach((item) => {
                    $('select[name=stud-input]').append(`<option value="${item.id}">${item.firstname} ${item.lastname} ${item.surname}</option>`);
                });
            });
        } else {
            await $.get(`api/students/`, function (data) {
                data.forEach((item) => {
                    $('select[name=stud-input]').append(`<option value="${item.id}">${item.surname} ${item.firstname.substring(0,1)}.${item.lastname.substring(0,1)}.</option>`);
                });
            });
        }
        updateTable('', id, '', $('input[name=score-zeroes-input]').prop('checked'), $('select[name=sort-input]').val());
    });
    // этап №3.
    $('select[name=stud-input]').change(async function () {
        const id = $(this).val();
        updateTable('', '', id, $('input[name=score-zeroes-input]').prop('checked'), $('select[name=sort-input]').val());
    });
    $('input[name=score-zeroes-input]').change(async function () {
        updateTable($('select[name=spec-input]').val(), $('select[name=group-input]').val(), $('select[name=stud-input]').val(), $(this).prop('checked'), $('select[name=sort-input]').val());
    });
    $('select[name=sort-input]').change(async function () {
        console.log($('select[name=sort-input]').val());
        updateTable($('select[name=spec-input]').val(), $('select[name=group-input]').val(), $('select[name=stud-input]').val(), $('input[name=score-zeroes-input]').prop('checked'), $(this).val());
    });
});

async function updateTable(spec, group, stud, onlyZeroes, sort) {
    $('tbody[name=marks-table]').empty();
    if (sort) {
    if (onlyZeroes) {
        if (stud) {
            await $.get(`api/get_marks_zeroes_studentSort/${stud}/${sort}`, function (data){
                data.result.forEach((item) => {
                    $('tbody[name=marks-table]').append(`<tr><td>${item.student_name}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject_name}</td><td>${item.startdate}</td><td>${item.enddate}</td><td class='marks-score-${item.score}'>${item.score}</td></tr>`);
                });
                if (data.result.length == 0) {
                    $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                };
            });
        } else if (group) {
            $.get(`api/get_marks_zeroes_groupSort/${group}/${sort}`, function (data) {
                data.result.forEach((item) => {
                    $('tbody[name=marks-table]').append(`<tr><td>${item.student_name}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject_name}</td><td>${item.startdate}</td><td>${item.enddate}</td><td class='marks-score-${item.score}'>${item.score}</td></tr>`);
                });
                if (data.result.length == 0) {
                    $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                };
            });
        } else if (spec) {
                $.get(`api/get_marks_zeroes_specSort/${spec}/${sort}`, function (data) {
                    data.result.forEach((item) => {
                        $('tbody[name=marks-table]').append(`<tr><td>${item.student_name}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject_name}</td><td>${item.startdate}</td><td>${item.enddate}</td><td class='marks-score-${item.score}'>${item.score}</td></tr>`);
                    });
                    if (data.result.length == 0) {
                        $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                    };
                });
            } else {
            await $.get(`api/marks_zeroes_sorted/?sorting=${sort}`, function (data){
                data.forEach((item) => {
                    $('tbody[name=marks-table]').append(`<tr><td>${item.student}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject}</td><td>${item.startdate}</td><td>${item.enddate}</td><td class='marks-score-${item.score}'>${item.score}</td></tr>`);
                });
                if (data.length == 0) {
                    $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                };
            });
        };
    } else {
        if (stud) {
            await $.get(`api/get_marks_studentSort/${stud}/${sort}`, function (data){
                data.result.forEach((item) => {
                    $('tbody[name=marks-table]').append(`<tr><td>${item.student_name}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject_name}</td><td>${item.startdate}</td><td>${item.enddate}</td><td>${item.score}</td></tr>`);
                });
                if (data.result.length == 0) {
                    $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                };
            });
        } else if (group) {
            $.get(`api/get_marks_groupSort/${group}/${sort}`, function (data) {
                data.result.forEach((item) => {
                    $('tbody[name=marks-table]').append(`<tr><td>${item.student_name}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject_name}</td><td>${item.startdate}</td><td>${item.enddate}</td><td>${item.score}</td></tr>`);
                });
                if (data.result.length == 0) {
                    $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                };
            });
        } else if (spec) {
                $.get(`api/get_marks_specSort/${spec}/${sort}`, function (data) {
                    data.result.forEach((item) => {
                        $('tbody[name=marks-table]').append(`<tr><td>${item.student_name}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject_name}</td><td>${item.startdate}</td><td>${item.enddate}</td><td>${item.score}</td></tr>`);
                    });
                    if (data.result.length == 0) {
                        $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                    };
                });
            } else {
            await $.get(`api/marks_sorted/?sorting=${sort}`, function (data){
                data.forEach((item) => {
                    $('tbody[name=marks-table]').append(`<tr><td>${item.student}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject}</td><td>${item.startdate}</td><td>${item.enddate}</td><td>${item.score}</td></tr>`);
                });
                if (data.length == 0) {
                    $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                };
            });
        };
    };
    } else {
    if (onlyZeroes) {
        if (stud) {
            await $.get(`api/get_marks_zeroes_student/${stud}`, function (data){
                data.result.forEach((item) => {
                    $('tbody[name=marks-table]').append(`<tr><td>${item.student_name}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject_name}</td><td>${item.startdate}</td><td>${item.enddate}</td><td class='marks-score-${item.score}'>${item.score}</td></tr>`);
                });
                if (data.result.length == 0) {
                    $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                };
            });
        } else if (group) {
            $.get(`api/get_marks_zeroes_group/${group}`, function (data) {
                data.result.forEach((item) => {
                    $('tbody[name=marks-table]').append(`<tr><td>${item.student_name}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject_name}</td><td>${item.startdate}</td><td>${item.enddate}</td><td class='marks-score-${item.score}'>${item.score}</td></tr>`);
                });
                if (data.result.length == 0) {
                    $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                };
            });
        } else if (spec) {
                $.get(`api/get_marks_zeroes_spec/${spec}`, function (data) {
                    data.result.forEach((item) => {
                        $('tbody[name=marks-table]').append(`<tr><td>${item.student_name}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject_name}</td><td>${item.startdate}</td><td>${item.enddate}</td><td class='marks-score-${item.score}'>${item.score}</td></tr>`);
                    });
                    if (data.result.length == 0) {
                        $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                    };
                });
            } else {
                await $.get(`api/marks_zeroes/`, function (data){
                    data.forEach((item) => {
                        $('tbody[name=marks-table]').append(`<tr><td>${item.student}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject}</td><td>${item.startdate}</td><td>${item.enddate}</td><td class='marks-score-${item.score}'>${item.score}</td></tr>`);
                    });
                    if (data.length == 0) {
                        $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                    };
                });
            };
        } else {
            if (stud) {
                await $.get(`api/get_marks_student/${stud}`, function (data){
                    data.result.forEach((item) => {
                        $('tbody[name=marks-table]').append(`<tr><td>${item.student_name}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject_name}</td><td>${item.startdate}</td><td>${item.enddate}</td><td>${item.score}</td></tr>`);
                    });
                    if (data.result.length == 0) {
                        $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                    };
                });
            } else if (group) {
                $.get(`api/get_marks_group/${group}`, function (data) {
                    data.result.forEach((item) => {
                        $('tbody[name=marks-table]').append(`<tr><td>${item.student_name}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject_name}</td><td>${item.startdate}</td><td>${item.enddate}</td><td>${item.score}</td></tr>`);
                    });
                    if (data.result.length == 0) {
                        $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                    };
                });
            } else if (spec) {
                    $.get(`api/get_marks_spec/${spec}`, function (data) {
                        data.result.forEach((item) => {
                            $('tbody[name=marks-table]').append(`<tr><td>${item.student_name}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject_name}</td><td>${item.startdate}</td><td>${item.enddate}</td><td>${item.score}</td></tr>`);
                        });
                        if (data.result.length == 0) {
                            $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                        };
                    });
                } else {
                await $.get(`api/marks/`, function (data){
                    data.forEach((item) => {
                        $('tbody[name=marks-table]').append(`<tr><td>${item.student}</td><td>${item.group}</td><td>${item.session}</td><td>${item.subject}</td><td>${item.startdate}</td><td>${item.enddate}</td><td>${item.score}</td></tr>`);
                    });
                    if (data.length == 0) {
                        $('tbody[name=marks-table]').append(`<tr><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td><td><hr></td></tr>`);
                    };
                });
            };
        };
    };
};